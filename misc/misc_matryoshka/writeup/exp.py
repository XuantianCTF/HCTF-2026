#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
exp.py — matryoshka 解题 PoC（按选手视角步骤化演示）

用法：
  python exp.py                     # 解本地 src/dist/ 下的附件（开发自测）
  python exp.py http://host:8080/   # 从部署实例下载附件（URL 会自动定位 RLO 文件名）
  python exp.py path/to/attachment  # 直接给本地附件路径

解题链条（每层五步）：
  1. 文件名 RLO 欺骗：os.listdir 拿到真实名（U+202E + 反转），glob("*.png") 匹配不到
  2. 魔数识别真实图片格式（PNG/GIF 混排，不能写死一种）
  3. 三明治分离：图片 + 密文碎片文本 + ZIP
     —— ZIP 起点用 EOCD 反推：S = eocd_pos - cd_offset - cd_size（不依赖魔数搜索）
  4. ZIP 加密三态：没加密直接解 / 伪加密修 GP flag bit0 / 真加密用 comment 里的钥匙
  5. comment 读密钥碎片 -> 解压进入下一层 -> 直到 END.txt
最后：KEY 倒序配对重组，与 CIPHER 逐字节 XOR（OTP）得 flag。
"""
import io
import os
import re
import sys
import zipfile
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

BASE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(BASE, "..", "src", "dist")

MAGICS = [
    (b"\x89PNG\r\n\x1a\n", "png"),
    (b"GIF87a", "gif"),
    (b"GIF89a", "gif"),
    (b"\xff\xd8\xff", "jpg"),
    (b"BM", "bmp"),
]
CIPHER_RE = re.compile(rb"MATRYOSHKA-CIPHER-FRAG (\d+)/(\d+)\n([0-9a-f]+)\n")
KEY_RE = re.compile(rb"MATRYOSHKA-KEY-FRAG (\d+)/(\d+)\n([0-9a-f]+)")


def zw_decode(text: str) -> str:
    """零宽字符解码：ZWSP(U+200B)=0 / ZWNJ(U+200C)=1，每 4 bit 一个 hex 字符。"""
    bits = "".join("0" if ch == "\u200b" else "1"
                   for ch in text if ch in ("\u200b", "\u200c"))
    return "".join("%x" % int(bits[i:i + 4], 2) for i in range(0, len(bits), 4))


def gif_palette_unsteg(gif: bytes) -> bytes:
    """从 GIF 全局色彩表 LSB 提取：MSK 魔数 + 1 字节长度 + 数据。"""
    packed = gif[10]
    if not packed & 0x80:
        raise ValueError("no global color table")
    bits = "".join(str(b & 1) for b in gif[13:13 + 32])
    if int(bits[:24], 2).to_bytes(3, "big") != b"MSK":
        raise ValueError("no MSK magic in gif palette LSB")
    plen = int(bits[24:32], 2)
    more = "".join(str(b & 1) for b in gif[13 + 32:13 + 32 + plen * 8])
    return int(more, 2).to_bytes(plen, "big")


def header(title):
    print("\n" + "=" * 62 + "\n%s\n" % title + "=" * 62)


def locate_zip(data: bytes) -> int:
    """EOCD 反推 zip 起点：CD 紧跟 local entries，EOCD 紧跟 CD。
    zip_start = eocd_pos - cd_size - cd_offset"""
    eocd = data.rfind(b"PK\x05\x06")
    if eocd < 0:
        raise ValueError("EOCD not found")
    cd_offset = int.from_bytes(data[eocd + 16:eocd + 20], "little")
    cd_size = int.from_bytes(data[eocd + 12:eocd + 16], "little")
    return eocd - cd_size - cd_offset


def defake_encrypt(zb: bytes) -> bytes:
    """伪加密修复：结构化清零 GP flag bit0（两处）"""
    data = bytearray(zb)
    eocd = bytes(data).rfind(b"PK\x05\x06")
    cd_offset = int.from_bytes(data[eocd + 16:eocd + 20], "little")
    pos = cd_offset
    while bytes(data[pos:pos + 4]) == b"PK\x01\x02":
        data[pos + 8:pos + 10] = (int.from_bytes(data[pos + 8:pos + 10], "little")
                                  & ~1).to_bytes(2, "little")
        local = int.from_bytes(data[pos + 42:pos + 46], "little")
        data[local + 6:local + 8] = (int.from_bytes(data[local + 6:local + 8], "little")
                                     & ~1).to_bytes(2, "little")
        name_len = int.from_bytes(data[pos + 28:pos + 30], "little")
        extra_len = int.from_bytes(data[pos + 30:pos + 32], "little")
        cmt_len = int.from_bytes(data[pos + 32:pos + 34], "little")
        pos += 46 + name_len + extra_len + cmt_len
    return bytes(data)


def load_attachment():
    """附件来源：命令行参数（URL 或路径），缺省取 src/dist/ 下唯一文件。"""
    if len(sys.argv) > 1:
        src = sys.argv[1]
        if src.startswith(("http://", "https://")):
            # 附件文件名带 U+202E，http.server 目录列表里 href 是 percent-encoded
            import html
            from urllib.parse import unquote
            listing = urllib.request.urlopen(src).read().decode("utf-8", "replace")
            links = [l for l in re.findall(r'href="([^"]+)"', listing)
                     if not l.startswith(("/", "?")) and l != ".."]
            if not links:
                raise SystemExit("目录列表里没找到附件: %r" % links)
            raw = links[0]
            name = unquote(html.unescape(raw))
            print("目录列表拿到真实文件名: %r" % name)
            print("  -> 含 U+202E(RIGHT-TO-LEFT OVERRIDE)，浏览器显示为: %s"
                  % name[1:][::-1])
            url = src.rstrip("/") + "/" + raw
            return name, urllib.request.urlopen(url).read()
        with open(src, "rb") as f:
            return os.path.basename(src), f.read()
    if not os.path.isdir(DIST):
        raise SystemExit("用法: python exp.py [附件URL或路径]（缺省找 src/dist/，"
                         "先在 src/ 下跑 python build.py 生成）")
    got = os.listdir(DIST)
    if len(got) != 1:
        raise SystemExit("src/dist/ 下应只有一个附件，实际: %r" % got)
    with open(os.path.join(DIST, got[0]), "rb") as f:
        return got[0], f.read()


def solve():
    header("Step 0 - 拿到的文件是什么？")

    name, data = load_attachment()
    print("文件名 %r" % name)
    print("  -> 含 U+202E(RIGHT-TO-LEFT OVERRIDE)，资源管理器显示为: %s"
          % name[1:][::-1])
    print("  -> Windows 按最后一个 '.' 取真实扩展名 %r，无关联程序，双击打不开"
          % ("." + name.rsplit(".", 1)[1]))
    print("  -> glob('*.png') 匹配不到它（真实扩展名不是 png）")

    c_frags, k_frags = {}, {}
    layer = 0

    while True:
        layer += 1
        header("Layer %d" % layer)

        fmt = next(ext for magic, ext in MAGICS if data.startswith(magic))
        print("[1] 魔数识别: 真实图片格式 = %s" % fmt)

        zstart = locate_zip(data)
        img_part, text_part, zip_part = data[:zstart], None, data[zstart:]
        # 文本夹在图片结束标记与 zip 之间，直接从整份字节里取标记行更稳
        m = CIPHER_RE.search(data)
        print("[2] 三明治分离: 图片 %d 字节 | zip 从偏移 %d 起，共 %d 字节"
              % (zstart, zstart, len(zip_part)))
        print("    图片尾部与 zip 之间的文本:")
        if m:
            i, n, hexfrag = int(m.group(1)), int(m.group(2)), m.group(3)
            print("    " + m.group(0).decode().strip().replace("\n", "\n    "))
            c_frags[i] = bytes.fromhex(hexfrag.decode())
        else:
            # 该层 cipher 不在明文里——台词让你"多看"这个 gif：调色板 LSB
            print("    " + data[:zstart].decode("utf-8", "ignore")
                  .strip().splitlines()[-1])
            frag = gif_palette_unsteg(data)
            print("    (这层没有明文碎片 -> 藏在 GIF 全局色彩表 LSB 里，"
                  "提取 MSK 魔数 + %d 字节碎片: %s)" % (len(frag), frag.hex()))
            c_frags[layer] = frag

        zf_raw = zipfile.ZipFile(io.BytesIO(zip_part))  # 不修 flag：comment/namelist 本就明文可读
        ctext = zf_raw.comment.decode("utf-8", "replace")
        m = re.search(r"MATRYOSHKA-KEY-FRAG (\d+)/(\d+)", ctext)
        ki, kn = int(m.group(1)), int(m.group(2))
        k = KEY_RE.search(zf_raw.comment)
        if k:
            khex = k.group(3)
        else:
            # kipfel 层：明文被吃光，完整密钥在最后一行的零宽字符里
            khex = zw_decode(ctext).encode()
        print("[3] archive comment 里的密钥碎片（comment 明文，无需解压即可读）:")
        shown = ctext.replace("\u200b", "[ZWSP]").replace("\u200c", "[ZWNJ]")
        print("    " + shown.replace("\n", "\n    "))
        if not k:
            print("    (最后一行看起来是空的——其实全是零宽字符，解码得密钥碎片 %s)"
                  % khex.decode())
        k_frags[ki] = bytes.fromhex(khex.decode())

        inner_names = zf_raw.namelist()
        # [4] 解压：先看 GP flag bit0 判断有没有加密标志，再区分伪/真
        encrypted_flag = bool(zf_raw.infolist()[0].flag_bits & 1)
        if not encrypted_flag:
            content = zf_raw.read(inner_names[0])
            print("[4] 这层 zip 没有任何加密，直接解压")
        else:
            try:
                zf = zipfile.ZipFile(io.BytesIO(defake_encrypt(zip_part)))
                content = zf.read(inner_names[0])
                print("[4] 伪加密：GP flag bit0 清零后解压成功")
            except Exception:
                print("[4] flag 清零后仍解不开 -> 这层是真加密（ZipCrypto），不是伪加密！")
                print("    密码挂在锁上：拿 comment 里的 KEY 碎片 hex 当密码")
                content = zf_raw.read(inner_names[0], pwd=khex)

        print("[5] 解压得到: %r" % inner_names)
        if "END.txt" in inner_names:
            end_text = bytes.fromhex(content.decode()).decode()
            print("\n".join("    | " + line for line in end_text.strip().splitlines()))
            break
        inner_name = inner_names[0]
        print("    下一层文件名 %r，资源管理器会显示为 %s"
              % (inner_name, inner_name[1:][::-1]))
        # 解压内容是 hex 文本（防止 DEFLATE stored block 把深层明文漏到最外层）
        data = bytes.fromhex(content.decode().strip())
        print("    (内容为 hex 文本，解码 %d 字节后进入下一层)" % len(data))

    header("Final - 碎片重组")
    n = len(c_frags)
    cipher = b"".join(c_frags[i] for i in range(1, n + 1))
    # KEY 与 CIPHER 倒序配对：comment 表面序号是层号，层 i 装的是第 (n+2-i)
    # 段 key（层 1 除外）——按表面序号直接拼只会 XOR 出乱码，需按 [1,N,N-1,..,2] 重排
    order = [1] + list(range(n, 1, -1))
    key = b"".join(k_frags[i] for i in order)
    print("CIPHER 按层序拼接; KEY 按倒序配对重排 %r" % order)
    flag = bytes(a ^ b for a, b in zip(cipher, key))
    print("\nFLAG: %s" % flag.decode())
    return 0


if __name__ == "__main__":
    sys.exit(solve())
