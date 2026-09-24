# -*- coding: utf-8 -*-
"""统一身份认证平台 · CTF 复刻后端（题2 切片：前端泄露 RSA 私钥）

入口均为登录页，登录本身永远失败"用户名或密码错误"：
  题2（本题考点）前端泄露 RSA 私钥：app.js 中硬编码 private_exponent，
      可解密 doc.html 调试记录里"拦截到的"管理员登录密文
  题1 同款网关绕过保留：/doc.html 被 nginx 403，但后端仍带老式路径解析
      （/sc/..;/doc.html），作为密文的获取通道；原题1 flag 槽位放置静态
      诱饵 fflag{}（判分不收）
  题3 请求头注入越权（/sc/api/authc/users 信任 loginUserId 等请求头）：
      保留漏洞面，flag 槽位为无害占位符
真 flag 由 seed.py 读取 FLAG 环境变量加密为密文，动态注入闭环在本容器内。
"""
import json
import sqlite3
import time
import uuid
from pathlib import Path

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse

BASE = Path(__file__).parent
DB_PATH = BASE / "data" / "cas.db"

app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)

# ----------------------------------------------------------------------
# 中间件：后端路径解析（复刻 Tomcat 行为：先剥离路径参数，再做点段归一化）
# 与题1（pathconfusion）同款的网关/后端解析差异——本题保留它作为
# doc.html（密文所在页）的获取通道：/sc/..;/doc.html
# ----------------------------------------------------------------------
def strip_path_params(path: str) -> str:
    """Tomcat 兼容：每个路径段中 ';' 之后的内容是路径参数，不参与路由。"""
    segs = [seg.split(";", 1)[0] if ";" in seg else seg for seg in path.split("/")]
    return "/".join(segs)


def remove_dot_segments(path: str) -> str:
    """RFC 3986 §5.2.4 remove_dot_segments。"""
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


@app.middleware("http")
async def normalize_path(request: Request, call_next):
    # uvicorn 已做百分号解码（scope["path"]），这里复刻老后端的两步归一化
    raw = request.scope.get("path", "/")
    normalized = remove_dot_segments(strip_path_params(raw))
    request.scope["path"] = normalized
    response = await call_next(request)
    return response


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
<div class="wrap">
  <h1>统一身份认证平台内部接口文档 v3.2.1</h1>
  <div class="warn">本文档仅限运维与对接方内部使用，生产环境已由网关屏蔽直接访问。</div>

  <h2>一、认证与票据</h2>
  <table>
    <tr><th>方法</th><th>路径</th><th>说明</th></tr>
    <tr><td>POST</td><td><code>/lyuapServer/v1/tickets</code></td><td>账密登录，发放 ST 票据（响应 code：NOUSER / USERDISABLED / PASSERROR / 成功返回 uid+vcodes）</td></tr>
    <tr><td>POST</td><td><code>/lyuapServer/v1/tickets/{ticket}</code></td><td>携 service 校验 ST 票据</td></tr>
    <tr><td>GET</td><td><code>/lyuapServer/UKey/getRandom</code></td><td>UKey 登录随机数</td></tr>
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

  <h2>三、开发调试记录（2026-03）</h2>
  <p>联调期间在网关上抓到一包<b>管理员测试账号</b>的登录请求，密码密文如下，公钥存于本地：</p>
  <p>fflag{d0t5egm3nt_byp4ss_4g41n} </p>
  <!-- <p><code id="ct">__CIPHERTEXT__</code></p> -->
  <p>注：密码域即口令全文，不做摘要；登录票据 loginToken 的明文格式为 TAG + 13 位毫秒时间戳，TAG 见前端常量表。</p>
</div>
</body>
</html>
"""


@app.get("/doc.html", response_class=HTMLResponse)
async def doc_html():
    ct = (BASE / "data" / "captured_login.txt").read_text().strip()
    html = DOC_HTML.replace("__CIPHERTEXT__", ct)
    # fflag{} 为静态诱饵（原题1 flag 槽位），无需替换；真 flag 在密文里
    return HTMLResponse(html)


# ----------------------------------------------------------------------
# 登录（永远失败：用户名或密码错误）
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# 登录页配置（复刻线上 /lyuapServer/loginType，附件已本地化）
# ----------------------------------------------------------------------
LOGIN_TYPE = json.loads((BASE / "config" / "loginType.json").read_text(encoding="utf-8"))


@app.get("/lyuapServer/loginType")
async def login_type():
    return LOGIN_TYPE


@app.post("/lyuapServer/v1/tickets")
async def tickets(request: Request):
    # 无论账号密码：一律按未注册/密码错误返回 NOUSER（前端渲染"用户名或密码错误。"）
    return JSONResponse(
        {"data": {"code": "NOUSER", "uid": "", "vcodes": ""}}, status_code=200
    )


@app.post("/lyuapServer/v1/tickets/{ticket}")
async def ticket_validate(request: Request, ticket: str):
    return JSONResponse({"code": "INVALID", "msg": "ticket 不存在或已过期"})


@app.get("/lyuapServer/UKey/getRandom")
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
