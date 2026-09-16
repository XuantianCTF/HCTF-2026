#!/usr/bin/env python3
# web_ua_checkin acceptance check: UA cloaking gate + base64 comment flag.
# Usage: python exp.py [base_url]      (default http://127.0.0.1:8089)
#
# Checks (against a running instance, started for example with):
#   php -S 127.0.0.1:8089 -t src            # fallback flag
#   FLAG="hctf{dyn_test}" php -S ...        # injected flag
import base64
import os
import re
import sys
import urllib.error
import urllib.request

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8089"
PRANK_URL = "https://www.bilibili.com/video/BV1sa4y1X7Ng/?share_source=copy_web&t=16"
IPHONE_UA = ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) "
             "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 "
             "Mobile/15E148 Safari/604.1")
IPAD_UA = ("Mozilla/5.0 (iPad; CPU OS 17_5 like Mac OS X) "
           "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 "
           "Mobile/15E148 Safari/604.1")
ANDROID_UA = ("Mozilla/5.0 (Linux; Android 14; Pixel 8) "
              "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 "
              "Mobile Safari/537.36")

results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))
    print("%s %s%s" % ("[PASS]" if ok else "[FAIL]", name,
                       (" - " + detail) if detail else ""))


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Disable auto-follow so the 302 gate is observable."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


OPENER = urllib.request.build_opener(NoRedirect)


def fetch(ua):
    headers = {"User-Agent": ua} if ua is not None else {}
    r = urllib.request.Request(BASE + "/", headers=headers)
    try:
        with OPENER.open(r, timeout=10) as resp:
            return resp.status, resp.read().decode("utf-8", "replace"), resp.headers
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace"), e.headers


# 1) gate: non-iPhone agents get 302 to the prank video, empty body, no flag leak
for label, ua in (("Android UA", ANDROID_UA), ("iPad UA (deliberate block)", IPAD_UA),
                  ("curl-like UA", "curl/8.5.1"), (".NET bot UA", None)):
    code, body, hdrs = fetch(ua)
    check("%s -> 302" % label, code == 302, "status=%d" % code)
    check("%s -> Location is prank URL" % label,
          (hdrs.get("Location") or "") == PRANK_URL, hdrs.get("Location") or "")
    check("%s -> empty body (flag not served)" % label, body == "", "len=%d" % len(body))

# 2) iPhone branch: 200 poster page, meme comment intact, flag in base64 comment
code, body, hdrs = fetch(IPHONE_UA)
check("iPhone UA -> 200", code == 200, "status=%d" % code)
check("iPhone UA -> poster page served", "Only iPhone" in body and "iPhone" in body)
check("meme comment intact", "\u6c42\u4f60\u4eec\u4e0d\u8981\u518d\u5632\u7b11\u8fd9\u4e9b\u9898\u76ee\u4e86" in body
      and "QWQ" in body)

# 3) decode the base64 line that sits right before the comment close "-->"
m = re.search(r"^[ \t]*([A-Za-z0-9+/]{8,}={0,2})[ \t]*\r?\n-->", body, re.M)
b64 = m.group(1) if m else ""
check("base64 line found in HTML comment", m is not None, b64)
flag = base64.b64decode(b64).decode("utf-8", "replace") if b64 else ""
check("decoded flag wrapped in hctf{}",
      re.fullmatch(r"hctf\{[^}]+\}", flag) is not None, flag)

# 4) if this shell carries the FLAG env var used to start the server, compare exactly
injected = os.environ.get("FLAG")
if injected:
    check("decoded flag == $FLAG (dynamic injection)", flag == injected,
          "flag=%s $FLAG=%s" % (flag, injected))

failed = [r for r in results if not r[1]]
print("\n%d/%d checks passed" % (len(results) - len(failed), len(results)))
sys.exit(1 if failed else 0)
