#!/usr/bin/env python3
# Usage: python exp.py [base_url]      (default http://127.0.0.1:8089)
import base64
import re
import sys
import urllib.request

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8089"
IPHONE_UA = ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) "
             "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 "
             "Mobile/15E148 Safari/604.1")

req = urllib.request.Request(BASE + "/", headers={"User-Agent": IPHONE_UA})
body = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", "replace")

m = re.search(r"([A-Za-z0-9+/]{20,}={0,2})\s*\r?\n-->", body)
if not m:
    sys.exit("no base64 flag line found before '-->' - wrong challenge?")
print(base64.b64decode(m.group(1)).decode())
