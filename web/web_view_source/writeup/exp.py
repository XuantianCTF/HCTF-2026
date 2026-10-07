#!/usr/bin/env python3
# Usage: python3 exp.py [base_url]      (default http://127.0.0.1:8080)
#
# 查看网页源代码，从 HTML 注释里取出 flag。
import re
import sys
import urllib.request

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8080").rstrip("/")

body = urllib.request.urlopen(BASE + "/", timeout=10).read().decode("utf-8", "replace")

m = re.search(r"FLAG:\s*(HCTF\{[^}]*\})", body)
if not m:
    sys.exit("[-] flag not found in page source - wrong challenge?")

print(m.group(1))
