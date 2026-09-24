# -*- coding: utf-8 -*-
"""统一身份认证平台 · CTF 复刻后端

三个考点（入口均为登录页，登录本身永远失败"用户名或密码错误"）：
  题1 路径穿越绕网关：/doc.html 被 nginx 网关 403，经 /sc/ 原样转发 + 后端
      路径参数剥离 + 点段归一化的解析差异可绕过（/sc/..;/doc.html）
  题2 前端泄露 RSA 私钥：app.js 中硬编码 private_exponent，可解密拦截到的
      登录密文（doc.html 调试记录 / 题目附件）
  题3 请求头注入越权：/sc/api/application/open/ssoLogin/ 无需认证发放会话，
      /sc/api/authc/users 信任 loginUserId / loginUserOrgId 请求头判身份
"""
import json
import os
import re
import sqlite3
import time
import uuid
from pathlib import Path

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse

BASE = Path(__file__).parent
DB_PATH = BASE / "data" / "cas.db"

# 独立部署版（headerauth）：题1 的 flag 默认置空（doc.html 注释里不再有 flag，
# 该注释行留白）；题2 密文在 seed.py 中换为假口令；本题 flag 为 FLAG3。
FLAG1 = os.environ.get("FLAG1", "")
FLAG2 = os.environ.get("FLAG2", "Admin@demo2026#Test")   # 独立部署：占位符，非 flag
FLAG3 = os.environ.get("FLAG") or os.environ.get("FLAG3", "hctf{h34d3r_1nj3ct10n_pwn3d_all}")

app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)

# ----------------------------------------------------------------------
# 【系统更新记录 2026-04】题1（路径穿越）事件后的整改：
#   升级后端，移除了老式（Tomcat 系）路径解析兼容层——不再剥离路径参数
#   （';' 之后内容）、不再做点段归一化。/sc/..;/doc.html 一类的网关绕过
#   在本版本已封堵（路由按原始路径精确匹配，未命中一律 404）。
#   以下两个函数为历史实现的留档，本版本不再注册为中间件。
# ----------------------------------------------------------------------
def strip_path_params(path: str) -> str:  # pragma: no cover - 已停用
    """（已停用）Tomcat 兼容：每个路径段中 ';' 之后的内容是路径参数。"""
    segs = [seg.split(";", 1)[0] if ";" in seg else seg for seg in path.split("/")]
    return "/".join(segs)


def remove_dot_segments(path: str) -> str:  # pragma: no cover - 已停用
    """（已停用）RFC 3986 §5.2.4 remove_dot_segments。"""
    out = []
    for seg in path.split("/"):
        if seg == ".":
            continue
        if seg == "..":
            if out and out[-1] != "":
                out.pop()
            continue
        out.append(seg)
    res = "/".join(out)
    if not res.startswith("/"):
        res = "/" + res
    if path.endswith(("/.", "/..")) and not res.endswith("/"):
        res += "/"
    return res or "/"


# ----------------------------------------------------------------------
# 数据库
# ----------------------------------------------------------------------
SUMMARY_FIELDS = [
    "userId", "userName", "account", "sex", "orgId", "orgName",
    "grade", "professional", "className", "status",
]

DETAIL_EXTRA = [
    "nation", "political", "idCard", "birthday", "nativePlace", "phone",
    "email", "qq", "wechat", "dormitory", "address", "emergencyContact",
    "emergencyPhone", "enrollDate", "enrollType", "studentType", "length",
    "campus", "building", "cardNo", "bankCard", "bankName", "scholarship",
    "loan", "award", "punish", "cet4", "cet6", "computer", "teacher",
    "counselor", "password", "salt", "createTime", "updateTime", "lastLogin",
    "loginCount", "source", "remark", "tag", "version", "deleted", "secretLevel",
    "description",
]


def db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def row_to_dict(r: sqlite3.Row, full: bool = False) -> dict:
    d = {k: r[k] for k in SUMMARY_FIELDS}
    if full:
        d.update({k: r[k] for k in DETAIL_EXTRA})
    return d


# ----------------------------------------------------------------------
# 题目 1：内部 API 文档页（nginx 网关上被 403，需路径穿越绕过）
# ----------------------------------------------------------------------
DOC_HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>统一身份认证平台 · 内部接口文档</title>
<style>
  body{font-family:"Microsoft YaHei",Arial,sans-serif;background:#f5f6f7;color:#333;margin:0;padding:24px;}
  .wrap{max-width:960px;margin:0 auto;background:#fff;padding:32px 40px;box-shadow:0 1px 4px rgba(0,0,0,.08);}
  h1{font-size:20px;border-bottom:2px solid #1f6fb2;padding-bottom:10px;color:#1f6fb2;}
  h2{font-size:16px;margin-top:28px;color:#1f6fb2;}
  table{width:100%;border-collapse:collapse;margin:10px 0;font-size:13px;}
  th,td{border:1px solid #ddd;padding:6px 10px;text-align:left;}
  th{background:#eef4fa;}
  code{background:#f0f0f0;padding:1px 5px;border-radius:3px;font-size:12px;}
  .warn{background:#fff7e6;border:1px solid #ffd591;padding:10px 14px;font-size:13px;}
</style>
</head>
<body>
<!-- TODO: 待网关放行方案评审后对外暴露（独立部署版：题1 注释已按规范移除） -->
<div class="wrap">
  <h1>统一身份认证平台内部接口文档 v3.2.1</h1>
  <div class="warn">本文档仅限运维与对接方内部使用，生产环境已由网关屏蔽直接访问。</div>

  <h2>一、认证与票据</h2>
  <table>
    <tr><th>方法</th><th>路径</th><th>说明</th></tr>
    <tr><td>POST</td><td><code>/authServer/v1/tickets</code></td><td>账密登录，发放 ST 票据（响应 code：NOUSER / USERDISABLED / PASSERROR / 成功返回 uid+vcodes）</td></tr>
    <tr><td>POST</td><td><code>/authServer/v1/tickets/{ticket}</code></td><td>携 service 校验 ST 票据</td></tr>
    <tr><td>GET</td><td><code>/authServer/UKey/getRandom</code></td><td>UKey 登录随机数</td></tr>
  </table>

  <h2>二、业务网关（/sc/ 前缀，经 Nginx 转发）</h2>
  <table>
    <tr><th>方法</th><th>路径</th><th>说明</th></tr>
    <tr><td>GET</td><td><code>/sc/api/application/open/ssoLogin/</code></td><td>单点登录跳转入口，302 并下发会话 Cookie（customsid）</td></tr>
    <tr><td>GET</td><td><code>/sc/api/authc/users</code></td><td>当前用户信息；管理端查询支持 name/orgId 等过滤与分页（pageSize 上限 100）</td></tr>
    <tr><td>GET</td><td><code>/sc/api/authc/users/{userId}</detail></code></td><td>用户详情（全字段，仅管理员）</td></tr>
    <tr><td>GET</td><td><code>/sc/api/authc/orgs</code></td><td>组织架构树</td></tr>
    <tr><td>GET</td><td><code>/sc/api/application/list</code></td><td>已接入应用列表</td></tr>
  </table>

  <h2>三、安全整改记录（2026-05）</h2>
  <p>针对此前内部通报的前端调试私钥泄露问题（INC-2026-0506），已完成整改：前端构建
  流水线已清理调试密钥常量并<b>轮换 RSA 密钥对</b>；历史联调调试记录与抓包密文
  已按整改要求全部清除，不再于本文档留存。</p>
</div>
</body>
</html>
"""


@app.get("/doc.html", response_class=HTMLResponse)
async def doc_html():
    # 独立部署版：题1 的注释 flag 已移除；题2 的调试密文已按整改清除（无需注入）
    return HTMLResponse(DOC_HTML)


# ----------------------------------------------------------------------
# 登录（永远失败：用户名或密码错误）
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# 登录页配置（复刻线上 /authServer/loginType，附件已本地化）
# ----------------------------------------------------------------------
LOGIN_TYPE = json.loads((BASE / "config" / "loginType.json").read_text(encoding="utf-8"))


@app.get("/authServer/loginType")
async def login_type():
    return LOGIN_TYPE


@app.post("/authServer/v1/tickets")
async def tickets(request: Request):
    # 无论账号密码：一律按未注册/密码错误返回 NOUSER（前端渲染"用户名或密码错误。"）
    return JSONResponse(
        {"data": {"code": "NOUSER", "uid": "", "vcodes": ""}}, status_code=200
    )


@app.post("/authServer/v1/tickets/{ticket}")
async def ticket_validate(request: Request, ticket: str):
    return JSONResponse({"code": "INVALID", "msg": "ticket 不存在或已过期"})


@app.get("/authServer/UKey/getRandom")
async def ukey_random():
    return JSONResponse({"data": {"random": uuid.uuid4().hex}})


# ----------------------------------------------------------------------
# 题目 3：信任请求头的越权接口
# ----------------------------------------------------------------------
@app.get("/sc/api/application/open/ssoLogin/")
async def sso_login(request: Request):
    """开放入口：无需任何认证，302 跳首页并下发会话。"""
    resp = RedirectResponse(url="/", status_code=302)
    resp.set_cookie("customsid", uuid.uuid4().hex + str(int(time.time() * 1000)))
    return resp


@app.get("/sc/api/authc/users")
async def authc_users(request: Request):
    """身份判定只信任请求头（网关侧假定已完成认证）—— 复刻真实信任缝隙。"""
    sid = request.cookies.get("customsid")
    if not sid:
        return JSONResponse({"code": 401, "msg": "未登录或会话已过期"}, status_code=401)

    uid = request.headers.get("loginUserId", "")
    org = request.headers.get("loginUserOrgId", "")
    if not uid:
        return JSONResponse({"code": 403, "msg": "无权访问"}, status_code=403)
    # 管理员约定：loginUserId=1 且 loginUserOrgId=-1
    is_admin = (uid == "1" and org == "-1")

    params = request.query_params
    name = params.get("name", "").strip()
    try:
        page = max(1, int(params.get("page", "1")))
        page_size = min(100, max(1, int(params.get("pageSize", "10"))))
    except ValueError:
        page, page_size = 1, 10

    conn = db()
    try:
        if not is_admin:
            # 普通身份只能看到自己（此处会话未绑定真实用户 → 空列表）
            rows = conn.execute(
                "SELECT * FROM users WHERE userId = ?", (uid,)
            ).fetchall()
        else:
            if name:
                rows = conn.execute(
                    "SELECT * FROM users WHERE userName LIKE ? OR account LIKE ?",
                    (f"%{name}%", f"%{name}%"),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM users LIMIT ? OFFSET ?",
                    (page_size, (page - 1) * page_size),
                ).fetchall()
        total = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    finally:
        conn.close()
    return JSONResponse({
        "code": 0, "msg": "success",
        "data": {
            "total": total,
            "records": [row_to_dict(r) for r in rows],
        },
    })


@app.get("/sc/api/authc/users/{user_id}")
async def authc_user_detail(request: Request, user_id: str):
    sid = request.cookies.get("customsid")
    if not sid:
        return JSONResponse({"code": 401, "msg": "未登录或会话已过期"}, status_code=401)
    uid = request.headers.get("loginUserId", "")
    org = request.headers.get("loginUserOrgId", "")
    is_admin = (uid == "1" and org == "-1")
    if not is_admin:
        return JSONResponse({"code": 403, "msg": "无权访问"}, status_code=403)

    conn = db()
    try:
        r = conn.execute("SELECT * FROM users WHERE userId = ?", (user_id,)).fetchone()
    finally:
        conn.close()
    if not r:
        return JSONResponse({"code": 404, "msg": "用户不存在"}, status_code=404)
    return JSONResponse({"code": 0, "msg": "success", "data": row_to_dict(r, full=True)})


@app.get("/sc/api/authc/orgs")
async def authc_orgs(request: Request):
    sid = request.cookies.get("customsid")
    if not sid:
        return JSONResponse({"code": 401, "msg": "未登录或会话已过期"}, status_code=401)
    return JSONResponse({"code": 0, "msg": "success", "data": [
        {"orgId": -1, "orgName": "系统管理员"},
        {"orgId": 1, "orgName": "计算机学院"},
        {"orgId": 2, "orgName": "机械工程学院"},
        {"orgId": 3, "orgName": "电气工程学院"},
        {"orgId": 4, "orgName": "经济管理学院"},
        {"orgId": 5, "orgName": "语言文学学院"},
        {"orgId": 6, "orgName": "数理学院"},
    ]})


@app.get("/sc/api/application/list")
async def application_list(request: Request):
    return JSONResponse({"code": 0, "msg": "success", "data": [
        {"appId": 101, "name": "教务系统", "url": "https://jw.example.edu.cn"},
        {"appId": 102, "name": "图书馆", "url": "https://lib.example.edu.cn"},
        {"appId": 103, "name": "网络教学平台", "url": "https://mooc.example.edu.cn"},
        {"appId": 104, "name": "一卡通", "url": "https://ecard.example.edu.cn"},
        {"appId": 105, "name": "宿舍报修", "url": "https://repair.example.edu.cn"},
    ]})


# ----------------------------------------------------------------------
# 兜底：记录前端 SPA 打到后端的未知路径（联调观察用）
# ----------------------------------------------------------------------
@app.api_route("/{rest:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
async def fallback(request: Request, rest: str):
    return JSONResponse({"code": 404, "msg": f"not found: {rest}"}, status_code=404)
