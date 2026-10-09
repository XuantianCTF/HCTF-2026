#!/usr/bin/env python3
import subprocess
import sys

ENC = [
    0x48, 0x43, 0x54, 0x46, 0x7B, 0x77, 0x33, 0x6C, 0x63, 0x30, 0x6D, 0x33, 0x5F,
    0x37, 0x30, 0x5F, 0x48, 0x43, 0x54, 0x46, 0x5F, 0x32, 0x30, 0x32, 0x36, 0x7D,
]

flag = "".join(chr(c) for c in ENC)
print(f"[+] flag = {flag}")

binary = sys.argv[1] if len(sys.argv) > 1 else "../attachment/signin.exe"


def run(cmd):
    return subprocess.run(
        cmd, input=flag + "\n", capture_output=True, text=True, timeout=10
    ).stdout


try:
    try:
        out = run([binary])
    except OSError:
        out = run(["wine", binary])
    print("[+] verify:", "Correct" in out)
except FileNotFoundError:
    print("[!] binary not built yet, run: docker build -t rev-signin ../attachment")
