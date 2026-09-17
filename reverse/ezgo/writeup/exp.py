#!/usr/bin/env python3
import subprocess
import sys

secret = [
    0x2f, 0x2c, 0x24, 0x2e, 0x1e, 0x15, 0x57, 0x03, 0x11, 0x06, 0x02,
    0x2d, 0x1f, 0x5f, 0x02, 0x37, 0x54, 0x01, 0x38, 0x0a, 0x0a, 0x15,
]

key = b"gopher"

flag = bytes(secret[i] ^ key[i % len(key)] for i in range(len(secret))).decode()
print(f"[+] flag = {flag}")

binary = sys.argv[1] if len(sys.argv) > 1 else "../attachment/ezgo"
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
    print("[!] binary not built yet, run: docker build -t rev-ezgo ../attachment")
