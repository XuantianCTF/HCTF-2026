#!/usr/bin/env python3
import base64
import subprocess
import sys

TABLE = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm0123456789+/"
STD = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

KEY = b"HCTF"

CIPHER = bytes([
    0x04, 0x17, 0x12, 0x1e, 0x03, 0x25, 0x2e, 0x36, 0x3a, 0x19, 0x17, 0x76,
    0x0c, 0x16, 0x65, 0x3f, 0x06, 0x33, 0x1f, 0x2b, 0x0c, 0x72, 0x6c, 0x74,
    0x0e, 0x1a, 0x6c, 0x75, 0x0e, 0x16, 0x04, 0x2a, 0x0c, 0x70, 0x64, 0x7b,
])

# 第一层：异或还原出自定义表编码后的字符串
encoded = bytes(CIPHER[i] ^ KEY[i % len(KEY)] for i in range(len(CIPHER))).decode()
print(f"[+] custom-b64 text = {encoded}")

# 第二层：把自定义表映射回标准 base64 表后解码
mapped = encoded.translate(str.maketrans(TABLE, STD))
flag = base64.b64decode(mapped).decode()
print(f"[+] flag = {flag}")

binary = sys.argv[1] if len(sys.argv) > 1 else "../attachment/baseNo"
try:
    out = subprocess.run(
        [binary],
        input=flag + "\n",
        capture_output=True,
        text=True,
        timeout=10,
    ).stdout
    print("[+] verify:", "Correct" in out)
except FileNotFoundError:
    print("[!] binary not built yet, run: docker build -t rev-baseno ../attachment")
