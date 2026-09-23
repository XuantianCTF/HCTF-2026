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
import asyncio
import base64
import json
import os
import random
import re
import sqlite3
import time
import uuid
from collections import defaultdict
from pathlib import Path

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse, PlainTextResponse, StreamingResponse

BASE = Path(__file__).parent
DB_PATH = BASE / "data" / "cas.db"

FLAG1 = os.environ.get("FLAG") or os.environ.get("FLAG1", "hctf{d0t5egm3nt_byp4ss_t0_doc}")
FLAG2 = os.environ.get("FLAG2", "Admin@demo2026#Test")   # 独立部署：占位符，非 flag
FLAG3 = os.environ.get("FLAG3", "已回收")                # 独立部署：占位符，非 flag

app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)

# ----------------------------------------------------------------------
# 中间件：后端路径解析（复刻 Tomcat 行为：先剥离路径参数，再做点段归一化）
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
    # 重建：保证以 / 开头
    res = "/".join(out)
    if not res.startswith("/"):
        res = "/" + res
    # 尾部点段清掉后保持目录语义
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

  <h2>三、开发调试记录（2026-03）</h2>
  <p><b>管理员测试账号</b>的登录请求，密码密文如下（RSA/None/PKCS1-v1_5）：</p>
  <p>hctf{d0t5egm3nt_byp4ss_t0_doc} </p>
  <!-- <p><code id="ct">__CIPHERTEXT__</code></p> -->
</div>
</body>
</html>
"""


@app.get("/doc.html", response_class=HTMLResponse)
async def doc_html():
    ct = (BASE / "data" / "captured_login.txt").read_text().strip()
    html = DOC_HTML.replace("__CIPHERTEXT__", ct)
    html = html.replace("hctf{d0t5egm3nt_byp4ss_t0_doc}", FLAG1)
    return HTMLResponse(html)


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
# 运维补偿通道（灰度下线中）—— 渐进门槛 + 碎片流
# ----------------------------------------------------------------------
HP_FLAG = os.environ.get("PC_HP_FLAG", "hctf{0ps_gr4nt_ch4nn3l_r3c0v3ry_0k}")
HP_CAP = float(os.environ.get("PC_HP_CAP", "3600"))    # 单流 wall-clock 上限（秒）
HP_MAX_LINES = 400                                     # 单流行数上限
HP_OPS_TOKEN = "OPS-VAL-7"

_hp_state = {"last_sent": {}, "flows": 0, "flows_ip": defaultdict(int)}
_hp_lock = asyncio.Lock()


def _hp_log(event, ip, extra=""):
    print(f"[honeypot] {event} ip={ip} {extra}", flush=True)


def _zeal(i: int) -> float:
    """芝诺间隔：8s 起步，×1.9 增长，封顶 110s。"""
    return min(110.0, 8.0 * (1.9 ** i))


def _frags() -> list:
    """凭据分段：内容段 + 永不到达的校验位（闭括号）段。"""
    body = HP_FLAG[:-1] if HP_FLAG.endswith("}") else HP_FLAG
    segs = [body[i:i + 9] for i in range(0, len(body), 9)]
    return segs + ["}"]


@app.get("/sc/api/application/open/opsGrant/")
async def ops_grant(request: Request):
    ip = request.client.host if request.client else "?"
    ua = request.headers.get("user-agent", "")

    # 限流：间隔 <1.5s → 429（时间戳打在响应发出时，见下）
    now = time.time()
    if now - _hp_state["last_sent"].get(ip, 0.0) < 1.5:
        _hp_log("ratelimited", ip, f"gap={now - _hp_state['last_sent'].get(ip, 0.0):.2f}")
        return JSONResponse({"code": 429, "msg": "too many requests"},
                            status_code=429, headers={"Retry-After": "2"})
    await asyncio.sleep(random.uniform(0.4, 2.2))    # 网关抖动
    _hp_state["last_sent"][ip] = time.time()

    # G1：浏览器 UA → 403 + base64 提示
    if ua.startswith("Mozilla"):
        _hp_log("gate1_block", ip, f"ua={ua[:40]}")
        return PlainTextResponse(base64.b64encode(
            "运维通道仅接受命令行工具直连，请使用 curl 重新发起。".encode("utf-8")
        ).decode("ascii"), status_code=403)

    # G2：缺头 → 401 + base32 提示
    tok = request.headers.get("x-ops-token")
    if tok is None:
        _hp_log("gate2_noheader", ip)
        return PlainTextResponse(base64.b32encode(
            b"ops channel requires header X-Ops-Token"
        ).decode("ascii"), status_code=401)

    # G3：值错 → 403 + GBK 当班码表（charset 标 utf-8，终端乱码，iconv -f GBK 还原）
    if tok != HP_OPS_TOKEN:
        _hp_log("gate3_badtoken", ip, f"tok={tok[:20]}")
        return Response(
            content="今日当班凭据表：VAL-7 组值班，凭据为 OPS-VAL-7（请以请求头 X-Ops-Token 携带）".encode("gbk"),
            status_code=403, media_type="text/plain; charset=utf-8")

    # 全过 → 并发护栏 → 碎片流
    async with _hp_lock:
        if _hp_state["flows"] >= 64 or _hp_state["flows_ip"][ip] >= 8:
            _hp_log("flow_rejected", ip, f"flows={_hp_state['flows']}")
            return JSONResponse({"code": 503, "msg": "通道并发已满，请稍后再试"}, status_code=503)
        _hp_state["flows"] += 1
        _hp_state["flows_ip"][ip] += 1
    _hp_log("flow_enter", ip, f"flows={_hp_state['flows']}")

    async def stream():
        start = time.time()
        ticket = f"TG-{uuid.uuid4().hex[:6].upper()}"
        try:
            for ln in (
                f"[ops] 工单已受理：{ticket}（通道灰度期，白名单校验通过）",
                "[ops] 风控复核：通过（0 风险项）",
                "[ops] 通道白名单已写入，本级凭据生效",
                "[ops] 凭据生成排队中，碎片将按队列顺序下发……",
            ):
                yield (ln + "\n").encode("utf-8")
            frags = _frags()
            n = len(frags)
            i = 0
            while True:
                if i >= HP_MAX_LINES or time.time() - start >= HP_CAP:
                    yield "[ops] 会话超时已断开，本次进度已作废，请重新发起（已收片段可保留）。\n".encode("utf-8")
                    _hp_log("flow_timeout", ip, f"frags={i}/{n} elapsed={time.time() - start:.0f}s")
                    break
                await asyncio.sleep(_zeal(i))
                if i >= n - 1:
                    # 校验位（闭括号）永远在生成队列前方
                    ahead = random.randint(3, 12)
                    yield f"frag {i + 1}/{n}: 校验位仍在生成队列，前方还有 {ahead} 人\n".encode("utf-8")
                    _hp_log("frag_zeno", ip, f"{i + 1}/{n} ahead={ahead}")
                else:
                    yield f"frag {i + 1}/{n}: {frags[i]}\n".encode("utf-8")
                    _hp_log("frag_sent", ip, f"{i + 1}/{n} {frags[i]}")
                i += 1
        finally:
            async with _hp_lock:
                _hp_state["flows"] -= 1
                _hp_state["flows_ip"][ip] -= 1

    return StreamingResponse(stream(), media_type="text/plain",
                             headers={"X-Accel-Buffering": "no", "Cache-Control": "no-store"})


# ----------------------------------------------------------------------
# 兜底：记录前端 SPA 打到后端的未知路径（联调观察用）
# ----------------------------------------------------------------------
@app.api_route("/{rest:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
async def fallback(request: Request, rest: str):
    return JSONResponse({"code": 404, "msg": f"not found: {rest}"}, status_code=404)
