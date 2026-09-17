#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build.py — matryoshka（套娃图片）misc 题生成脚本

题目结构（共 N 层，从外到内）：
  layer_i = [图片字节] + [密文碎片 c_i 文本] + [ZIP(DEFLATE, comment=密钥碎片 k_i, 内含 layer_{i+1})]
  最内层 zip 内含 END.txt + prize.png（终点标记）

考点叠加：
  1. RLO 文件名欺骗：真实名 = U+202E + 显示名反转（显示 "{i}.{ext}"，真实如 "gnp.{i}"）
  2. 多格式图片 polyglot：PNG/GIF/JPG/BMP 尾部追加数据，解码器读到各自结束标记即停
  3. ZIP 伪加密：local file header(+6) 与 central directory(+8) 的 GP flag bit0 置 1
  4. DEFLATE 压缩：深层碎片不以明文暴露在最外层文件流中（挡 strings/binwalk 短路）
  5. 碎片重组：密文/密钥各均分 N 段带 [i/N] 序号，收齐 XOR（OTP）还原 flag

用法：
  python build.py            # FLAG 环境变量缺省时用测试 flag
  FLAG=hctf{...} python build.py
"""
import io
import os
import sys
import zlib
import random
import shutil
import zipfile
import secrets

sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")
DIST = os.path.join(BASE, "dist")

# 每层图片（层号 -> 文件名，可增删；层数 = 列表长度）
LAYERS = ["l1.png", "l2.gif", "l3.png", "l4.gif", "l5.png"]
END_FILES = {"END.txt": None, "prize.png": "prize.png"}  # None -> 内置文本

# 真加密层（其余层伪加密）：ZipCrypto 密码 = 该层 zip 自身 comment 携带的
# KEY 碎片 hex——解压软件表现与伪加密层一样（弹密码框），但改 flag 解不开，
# 钥匙就挂在 comment 上。设为 None 则不真加密。
REAL_ENCRYPT_LAYER = 3

# 伪加密层（GP flag bit0 置 1、数据明文）。不在本表且非真加密的层 zip 完全
# 干净（无任何加密标志），直接解压。层 1 保留伪加密当第一层教学点。
FAKE_ENCRYPT_LAYERS = [1]

# kipfel 吃密钥层：该层 comment 不直接给明文密钥，而是逐行"被吃掉"的动画
# （可见前缀越来越短，吃掉的字符用点代替），最后一行用零宽字符完整编码密钥。
# 零宽方案：U+200B(ZWSP)=0 / U+200C(ZWNJ)=1，每 4 bit 编码一个 hex 字符；
# 动画行泄漏的可见前缀可当解码结果的校验。设为 None 则所有层明文直给。
KIPFEL_LAYER = 4

# GIF 调色板隐写层：该层的 CIPHER 碎片不拼在字节流明文里，而是藏进 GIF
# 全局色彩表的 LSB（每条目 R/G/B 各 1 bit，编码 MSK 魔数 + 1 字节长度 +
# 数据）；明文位置只留一句台词提示"多看"这个 gif。设为 None 则全部明文。
GIF_STEG_LAYER = 2
GIF_STEG_HINT = "kipfel可爱捏，好看，爱看，多看"

TEST_FLAG = "hctf{matry0shka_p0lygl0t_r10_deception}"

MAGICS = [
    (b"\x89PNG\r\n\x1a\n", "png"),
    (b"GIF87a", "gif"),
    (b"GIF89a", "gif"),
    (b"\xff\xd8\xff", "jpg"),
    (b"BM", "bmp"),
]

RLO = "\u202e"  # RIGHT-TO-LEFT OVERRIDE


def xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def detect_ext(data: bytes) -> str:
    for magic, ext in MAGICS:
        if data.startswith(magic):
            return ext
    raise ValueError("unknown image format (magic): %r" % data[:8])


def rlo_name(i: int, ext: str) -> str:
    """真实文件名：U+202E + 显示名反转。显示 "1.png" -> 真实 "\u202Egnp.1" """
    display = "%d.%s" % (i, ext)
    return RLO + display[::-1]


def split_n(data: bytes, n: int):
    """均分 n 段，余数摊进前面的段"""
    base, rem = divmod(len(data), n)
    out, pos = [], 0
    for k in range(n):
        size = base + (1 if k < rem else 0)
        out.append(data[pos:pos + size])
        pos += size
    return out


# ---------------------------------------------------------------- zip 伪加密

def _patch_gp_flags(zb: bytes, set_bit: bool) -> bytes:
    """结构化遍历 zip：置位/清零每条目 local(+6) 与 central(+8) 的 GP flag bit0。

    不做朴素签名搜索——DEFLATE 流里可能偶然出现 PK\\x03\\x04 字节序列，
    误改会破坏压缩数据。这里从 EOCD 反查 central directory 逐条精确修改。
    """
    data = bytearray(zb)
    eocd = bytes(data).rfind(b"PK\x05\x06")
    if eocd < 0:
        raise ValueError("EOCD not found")
    cd_offset = int.from_bytes(data[eocd + 16:eocd + 20], "little")
    pos = cd_offset
    n_entries = 0
    while bytes(data[pos:pos + 4]) == b"PK\x01\x02":
        for off in (pos + 8,):  # central: GP flag 偏移 +8
            flag = int.from_bytes(data[off:off + 2], "little")
            flag = (flag | 0x0001) if set_bit else (flag & ~0x0001)
            data[off:off + 2] = flag.to_bytes(2, "little")
        local = int.from_bytes(data[pos + 42:pos + 46], "little")
        off = local + 6  # local: GP flag 偏移 +6
        flag = int.from_bytes(data[off:off + 2], "little")
        flag = (flag | 0x0001) if set_bit else (flag & ~0x0001)
        data[off:off + 2] = flag.to_bytes(2, "little")
        name_len = int.from_bytes(data[pos + 28:pos + 30], "little")
        extra_len = int.from_bytes(data[pos + 30:pos + 32], "little")
        cmt_len = int.from_bytes(data[pos + 32:pos + 34], "little")
        pos += 46 + name_len + extra_len + cmt_len
        n_entries += 1
    if n_entries == 0:
        raise ValueError("no central directory entries")
    return bytes(data)


def fake_encrypt(zb: bytes) -> bytes:
    return _patch_gp_flags(zb, set_bit=True)


# ---------------------------------------------------------------- ZipCrypto 真加密

class _ZipCrypto:
    """PKWARE 传统 ZipCrypto。标准库只能读不能写，这里实现加密侧。
    解密侧 7-Zip / WinRAR / python zipfile(pwd=...) 全部原生支持。

    注意单步 CRC 必须用 register 级 primitive（(c>>8)^T[(c^b)&0xff]，无
    init/final 取反），不能用 zlib.crc32 的应用层链式语义——那是取反过的
    结果，两者不等价，会导致密钥流从密码初始化就分叉。"""

    _TABLE = None

    def __init__(self, password: bytes):
        self.k0, self.k1, self.k2 = 0x12345678, 0x23456789, 0x34567890
        for b in password:
            self._update(b)

    @classmethod
    def _crc(cls, c: int, b: int) -> int:
        if cls._TABLE is None:
            table = []
            for i in range(256):
                x = i
                for _ in range(8):
                    x = (x >> 1) ^ (0xEDB88320 if x & 1 else 0)
                table.append(x)
            cls._TABLE = table
        return ((c >> 8) ^ cls._TABLE[(c ^ b) & 0xff]) & 0xffffffff

    def _update(self, b: int):
        self.k0 = self._crc(self.k0, b)
        self.k1 = (self.k1 + (self.k0 & 0xff)) & 0xffffffff
        self.k1 = (self.k1 * 134775813 + 1) & 0xffffffff
        self.k2 = self._crc(self.k2, self.k1 >> 24)

    def stream(self, data: bytes) -> bytes:
        out = bytearray()
        for b in data:
            t = self.k2 | 2
            out.append(b ^ (((t * (t ^ 1)) >> 8) & 0xff))
            self._update(b)
        return bytes(out)


def real_encrypt(zb: bytes, password: bytes) -> bytes:
    """真加密：对 local header 后的压缩数据流做 ZipCrypto（前置 12 字节
    encryption header，末字节为原数据 CRC32 高字节作校验），并置 GP flag
    bit0；csize +12 需联动 local(+18)、central(+20) 与 EOCD cd_offset。
    逐条目处理，每加密一个条目重建字节串后重扫（偏移已失效）。"""
    while True:
        data = bytearray(zb)
        eocd = bytes(data).rfind(b"PK\x05\x06")
        cd_offset = int.from_bytes(data[eocd + 16:eocd + 20], "little")
        pos, target = cd_offset, None
        while bytes(data[pos:pos + 4]) == b"PK\x01\x02":
            if not int.from_bytes(data[pos + 8:pos + 10], "little") & 1:
                target = pos
                break
            nl = int.from_bytes(data[pos + 28:pos + 30], "little")
            el = int.from_bytes(data[pos + 30:pos + 32], "little")
            cl = int.from_bytes(data[pos + 32:pos + 34], "little")
            pos += 46 + nl + el + cl
        if target is None:
            return zb  # 所有条目均已加密

        crc = int.from_bytes(data[target + 16:target + 20], "little")
        csize = int.from_bytes(data[target + 20:target + 24], "little")
        local = int.from_bytes(data[target + 42:target + 46], "little")
        nl = int.from_bytes(data[local + 26:local + 28], "little")
        el = int.from_bytes(data[local + 28:local + 30], "little")
        doff = local + 30 + nl + el
        header = os.urandom(11) + bytes([(crc >> 24) & 0xff])
        enc = _ZipCrypto(password).stream(header + bytes(data[doff:doff + csize]))

        # 先改 central 与 local 的字段（均在数据区之前，不影响坐标）
        data[target + 8:target + 10] = (
            int.from_bytes(data[target + 8:target + 10], "little") | 1
        ).to_bytes(2, "little")
        data[target + 20:target + 24] = (csize + 12).to_bytes(4, "little")
        data[local + 6:local + 8] = (
            int.from_bytes(data[local + 6:local + 8], "little") | 1
        ).to_bytes(2, "little")
        data[local + 18:local + 22] = (csize + 12).to_bytes(4, "little")
        # 替换数据区（长度 +12），再修 EOCD 的 cd_offset（central 整体后移）
        data = bytearray(bytes(data[:doff]) + enc + bytes(data[doff + csize:]))
        eocd = bytes(data).rfind(b"PK\x05\x06")
        data[eocd + 16:eocd + 20] = (cd_offset + 12).to_bytes(4, "little")
        zb = bytes(data)


# ---------------------------------------------------------------- 层构造

CIPHER_MARK = "MATRYOSHKA-CIPHER-FRAG"
KEY_MARK = "MATRYOSHKA-KEY-FRAG"


def cipher_frag_text(i: int, n: int, frag: bytes) -> bytes:
    if i == GIF_STEG_LAYER:
        return ("\n%s\n" % GIF_STEG_HINT).encode("utf-8")
    return ("\n%s %d/%d\n%s\n" % (CIPHER_MARK, i, n, frag.hex())).encode()


def gif_palette_steg(gif: bytes, payload: bytes) -> bytes:
    """把 payload 藏进 GIF 全局色彩表每个字节通道的 LSB。
    编码：'MSK' 魔数 + 1 字节长度 + 数据，MSB-first，按条目 R,G,B 顺序铺开。
    只动调色板低位（每通道 ±1，视觉无损），帧数据与文件结构不动。"""
    data = bytearray(gif)
    packed = data[10]  # Logical Screen Descriptor 的 packed 字段
    if not packed & 0x80:
        raise ValueError("gif has no global color table")
    size = 2 << (packed & 0x07)  # 条目数 = 2^(flag+1)
    bits = "".join(format(b, "08b")
                   for b in b"MSK" + bytes([len(payload)]) + payload)
    if len(bits) > size * 3:
        raise ValueError("palette too small for payload")
    for i, b in enumerate(bits):
        off = 13 + i  # GIF 头 6 + LSD 7，全局色彩表紧随
        data[off] = (data[off] & 0xFE) | int(b)
    return bytes(data)


def key_frag_comment(i: int, n: int, frag: bytes) -> bytes:
    hexkey = frag.hex()
    if i == KIPFEL_LAYER:
        return kipfel_comment(i, n, hexkey).encode("utf-8")
    return ("%s %d/%d\n%s" % (KEY_MARK, i, n, hexkey)).encode()


_ZW_BITS = {"0": "\u200b", "1": "\u200c"}


def zw_encode(hex_str: str) -> str:
    """零宽字符编码：ZWSP=0 / ZWNJ=1，每个 hex 字符 4 bit。"""
    return "".join(_ZW_BITS[b] for c in hex_str
                   for b in format(int(c, 16), "04b"))


def kipfel_comment(i: int, n: int, hex_key: str) -> str:
    """kipfel 层 comment：密钥被逐行吃掉，最后一行零宽编码完整密钥。
    点数 = 已被吃掉的字符数；开场就被吃掉至少一半（存活 1~total/2），
    明文永远只能看到小半截。"""
    total = len(hex_key)
    alive0 = random.randint(1, total // 2)
    lines = ["%s %d/%d" % (KEY_MARK, i, n),
             "你来晚啦，密钥已经被kipfel吃掉一些了>w<"]
    for alive in range(alive0, 0, -1):
        eaten = total - alive
        lines.append(hex_key[:alive] + random.choice(">-") + "." * eaten)
        if alive > 1 and random.random() < 0.4:  # 挣扎一下，同级再来一行
            lines.append(hex_key[:alive] + random.choice(">-") + "." * eaten)
    lines.append("-" + "." * total)
    lines.append(zw_encode(hex_key))
    return "\n".join(lines)


def make_zip(files: dict, comment: bytes, real_password=None,
             fake: bool = False) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, content in files.items():
            # 内容先 hex 编码：图片等已压缩数据 DEFLATE 压不动时会输出 stored
            # block 原样保留，深层的碎片标记与 comment 会明文暴露在最外层文件
            # （strings 一把梭短路递归）。hex 后字符集仅 16 个，DEFLATE 必然真
            # 实压缩；附带收益是 binwalk 认不出 hex 里的下一层魔数。
            zf.writestr(name, content.hex().encode())
        zf.comment = comment
    zb = buf.getvalue()
    if real_password is not None:
        return real_encrypt(zb, real_password)
    if fake:
        return fake_encrypt(zb)
    return zb


def build():
    flag = os.environ.get("FLAG", TEST_FLAG).encode()
    n = len(LAYERS)

    key = secrets.token_bytes(len(flag))
    cipher = xor(flag, key)
    c_frags = split_n(cipher, n)
    k_frags = split_n(key, n)

    images = []
    for fname in LAYERS:
        with open(os.path.join(ASSETS, fname), "rb") as f:
            images.append(f.read())

    end_files = {}
    for name, src in END_FILES.items():
        if src is None:
            end_files[name] = (
                "恭喜，你已经剥到最里层了。\n"
                "现在你应该收集齐了 %d 段 CIPHER 碎片和 %d 段 KEY 碎片。\n"
                "把它们各自按序号拼起来，然后……你知道该做什么。\n" % (n, n)
            ).encode("utf-8")
        else:
            with open(os.path.join(ASSETS, src), "rb") as f:
                end_files[name] = f.read()

    # 从内向外：layer_n 的 zip 装终点文件，layer_i 的 zip 装 layer_{i+1}
    inner_files = end_files
    for i in range(n, 0, -1):
        img = images[i - 1]
        ext = detect_ext(img)
        if i == GIF_STEG_LAYER:
            if ext != "gif":
                raise ValueError("GIF_STEG_LAYER %d 的图片不是 gif" % i)
            img = gif_palette_steg(img, c_frags[i - 1])
        # KEY 倒序配对：comment 标记仍写层号 i，但层 i 装的是第 (n+2-i) 段
        # key（层 1 除外）——层 2 装第 N 段、层 3 装第 N-1 段……即除层 1 外
        # 倒序。层 3 真加密密码、层 4 kipfel 吃的密钥都随之变成
        # "自己 comment 携带的那段"，自洽不破。
        key_idx = 1 if i == 1 else n + 2 - i
        pwd = (k_frags[key_idx - 1].hex().encode()
               if i == REAL_ENCRYPT_LAYER else None)
        nxt = make_zip(inner_files,
                       key_frag_comment(i, n, k_frags[key_idx - 1]),
                       real_password=pwd,
                       fake=(i in FAKE_ENCRYPT_LAYERS))
        layer = img + cipher_frag_text(i, n, c_frags[i - 1]) + nxt
        inner_files = {rlo_name(i, ext): layer}
        tag = (" REAL-ENCRYPTED(pwd=own key frag)" if pwd else "") + \
              (" FAKE-ENCRYPTED" if i in FAKE_ENCRYPT_LAYERS else "") + \
              (" KIPFEL(key in zero-width)" if i == KIPFEL_LAYER else "") + \
              (" GIF-PALETTE-STEG(cipher)" if i == GIF_STEG_LAYER else "")
        print("[layer %d] image=%s display=%d.%s real=%r size=%d%s"
              % (i, LAYERS[i - 1], i, ext, rlo_name(i, ext), len(layer), tag))

    if os.path.isdir(DIST):
        try:
            shutil.rmtree(DIST)
        except PermissionError as e:
            print("错误: dist 里的旧附件正被其他程序占用（Bandizip/7-Zip/预览"
                  "窗格/看图工具？），请关闭后重跑 build.py。\n%r" % e)
            return 1
    os.makedirs(DIST)
    ((name, content),) = inner_files.items()
    out = os.path.join(DIST, name)
    with open(out, "wb") as f:
        f.write(content)

    print()
    print("flag        : %s" % flag.decode())
    print("layers      : %d" % n)
    print("output      : dist/ (display name shows as 1.%s)" % detect_ext(images[0]))
    print("output real : %r" % name)
    print("size        : %d bytes" % len(content))
    return 0


if __name__ == "__main__":
    sys.exit(build())
