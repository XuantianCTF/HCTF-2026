#!/usr/bin/env python3
import base64
import os
import sys
import zipfile

SECRET = "PS0mKRQaVTsHXkIbMBpVOxMcQwtbKw8RQBotWwEQF1RECg8="
MASK = b"unrooted"


def decrypt() -> str:
    data = base64.b64decode(SECRET)
    return bytes(data[i] ^ MASK[i % len(MASK)] for i in range(len(data))).decode()


def secret_in_apk(path: str) -> bool:
    if not os.path.isfile(path):
        return False
    with zipfile.ZipFile(path) as apk:
        for name in apk.namelist():
            if name.endswith("libunrooted.so") and SECRET.encode() in apk.read(name):
                return True
    return False


def main() -> int:
    flag = decrypt()
    print(f"[+] flag: {flag}")

    apk = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "attachment", "unrooted.apk"
    )
    if os.path.isfile(apk):
        ok = secret_in_apk(apk)
        print(f"[{'+' if ok else '!'}] secret found in {apk}: {ok}")
        return 0 if ok else 1

    print(f"[i] APK not present ({apk}); skip binary verification")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
