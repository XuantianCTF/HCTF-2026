"""CTF 新手课堂 —— Web 入门五讲（PPT 式新手引导题）

路由一览：
  /              封面
  /lesson/{1-5}  五课，每课一个知识点，lessons/*.md 渲染成白色极简幻灯片
  /exam          结课测试：五个文本框，客户端拼出 前缀{碎片1_..._碎片5}
  /robots.txt    第三课素材：Disallow 路径引出 /hidden-notes/
  /hidden-notes/ 第三课碎片所在页（教师备忘）
  /api/learn/{n} 「我已学会」打卡按钮 -> 发假碎片（蜜罐，按课号可追溯）
  /api/lesson5   第五课素材：只收 POST -> 发真碎片

真 flag 来自 FLAG 环境变量（平台 checker 注入，leet 隐写队标），
要求内容恰好 5 段下划线分隔（Rune 模板 const TEMPLATE = "a_b_c_d_e"，
leet 只替换字母数字，下划线原样保留），启动时拆成五块散落各课。
题内不做校验：末页只负责拼出完整 flag，对错与「老实学……」提示
由平台侧 checker（ret2shell-docs/checker_xinshouketang.rx）返回。
"""
import html
import os
import re

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles

BASE = os.path.dirname(os.path.abspath(__file__))

# ---- FLAG：读环境变量并拆成五块碎片（启动即校验，格式错直接拒绝起服务） ----
_RAW_FLAG = os.environ.get("FLAG", "HCTF{we1c0me_t0_web_ctf_2026}")
_FLAG_RE = re.fullmatch(r"([A-Za-z0-9]+)\{(.+)\}", _RAW_FLAG)
if not _FLAG_RE:
    raise RuntimeError(
        f"FLAG 环境变量格式错误：{_RAW_FLAG!r}，应为 前缀{{五段下划线分隔}}，"
        f"如 HCTF{{a_b_c_d_e}}（Rune checker 的 TEMPLATE 需一致）")
FLAG_PREFIX = _FLAG_RE.group(1)
_PIECES = _FLAG_RE.group(2).split("_")
if len(_PIECES) != 5:
    raise RuntimeError(
        f"FLAG 内容需恰好 5 段（用 _ 分隔），当前 {len(_PIECES)} 段：{_RAW_FLAG!r}")

# 五课：知识点名 / 真碎片（来自 FLAG 拆分）/ 假碎片（打卡按钮发的蜜罐）
# 假碎片与真碎片同长度量级、随机 hex，肉眼无法区分，平台 checker 按
# 精确值识别并回「老实学……，很无趣吧」
LESSONS = {
    1: {"name": "查看源代码", "real": _PIECES[0], "fake": "src-4c8e"},
    2: {"name": "HTTP 响应头", "real": _PIECES[1], "fake": "hdr-b3d7"},
    3: {"name": "robots.txt", "real": _PIECES[2], "fake": "rbt-e9a1"},
    4: {"name": "Cookie", "real": _PIECES[3], "fake": "ck-62f4"},
    5: {"name": "POST 请求", "real": _PIECES[4], "fake": "post-ad05"},
}

app = FastAPI(title="CTF 新手课堂", docs_url=None, redoc_url=None,
              openapi_url=None)


# ---------------------------------------------------------------- markdown
# 迷你渲染器：只支持本课题面用到的子集（# 标题 / 段落 / 无序列表 /
# > 引用 / **加粗** / `行内代码`），先整体转义再变换，无 XSS 面。
_BOLD = re.compile(r"\*\*(.+?)\*\*")
_CODE = re.compile(r"`([^`]+)`")


def _inline(s: str) -> str:
    s = html.escape(s, quote=False)
    s = _CODE.sub(r"<code>\1</code>", s)
    s = _BOLD.sub(r"<strong>\1</strong>", s)
    return s


def render_md(text: str) -> str:
    out, para, lst, quote = [], [], [], []

    def flush():
        if para:
            out.append("<p>" + "<br>\n".join(_inline(x) for x in para) + "</p>")
            para.clear()
        if lst:
            out.append("<ul>\n" +
                       "\n".join(f"<li>{_inline(x)}</li>" for x in lst) +
                       "\n</ul>")
            lst.clear()
        if quote:
            out.append("<blockquote>" +
                       "<br>\n".join(_inline(x) for x in quote) +
                       "</blockquote>")
            quote.clear()

    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip():
            flush()
            continue
        m = re.match(r"^(#{1,3})\s+(.*)", line)
        if m:
            flush()
            lv = len(m.group(1))
            out.append(f"<h{lv}>{_inline(m.group(2))}</h{lv}>")
            continue
        if line.startswith(">"):
            flush()
            quote.append(line[1:].lstrip())
            continue
        m = re.match(r"^[-*]\s+(.*)", line)
        if m:
            flush()
            lst.append(m.group(1))
            continue
        if lst or quote:
            flush()
        para.append(line)
    flush()
    return "\n".join(out)


def lesson_md(name: str) -> str:
    with open(os.path.join(BASE, "lessons", name), encoding="utf-8") as f:
        return render_md(f.read())


# ---------------------------------------------------------------- 页面壳
SHELL = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · CTF 新手课堂</title>
<link rel="stylesheet" href="/static/style.css">
</head>
<body>
<header class="top">
  <div class="brand">CTF 新手课堂<span class="sub">Web 入门 · 五讲</span></div>
  <div class="pageno">{pageno}</div>
</header>
<main class="slide">
{body}
</main>
<footer class="nav">
{nav}
</footer>
<script src="/static/app.js"></script>
</body>
</html>"""


def nav_row(prev_href="", prev_text="上一页",
            mid="", next_href="", next_text="下一页") -> str:
    prev = (f'<a class="btn nav-prev" href="{prev_href}">{prev_text}</a>'
            if prev_href else "<span></span>")
    nxt = (f'<a class="btn primary nav-next" href="{next_href}">{next_text}</a>'
           if next_href else "<span></span>")
    return f'<div class="nav-left">{prev}</div>\n<div class="nav-mid">{mid}</div>\n<div class="nav-right">{nxt}</div>'


def page(title: str, pageno: str, body: str, nav: str) -> str:
    return SHELL.format(title=html.escape(title), pageno=html.escape(pageno),
                        body=body, nav=nav)


# ---------------------------------------------------------------- 页面
ROBOTS = """\
# 新手课堂 robots.txt
# 这个文件是给搜索引擎爬虫看的「游客须知」：哪些路径欢迎光临，哪些请不要碰

User-agent: *
Disallow: /api/
Disallow: /hidden-notes/

# 提示：被 Disallow 的路径，值得每一位同学亲自「勿入」一次
"""


@app.get("/", response_class=HTMLResponse)
async def cover():
    body = f'<article class="md">{lesson_md("cover.md")}</article>'
    return HTMLResponse(page("封面", "01 / 07 · 封面", body,
                             nav_row(next_href="/lesson/1", next_text="开始上课")))


@app.get("/lesson/{n}", response_class=HTMLResponse)
async def lesson(n: int):
    if n not in LESSONS:
        return HTMLResponse("<h1>404</h1><p>没有这一课，<a href='/'>回课堂</a>。</p>",
                            status_code=404)
    le = LESSONS[n]
    content = lesson_md(f"{n}.md")
    if n == 1:  # 第一课碎片：HTML 注释，看源代码才能发现
        content += (
            "\n<!--\n"
            f"  第 1 块：{le['real']}\n"
            "  能在源代码里看到这行注释，第一课就算学会了\n"
            "-->\n"
        )
    prev_href = "/" if n == 1 else f"/lesson/{n - 1}"
    next_href = f"/lesson/{n + 1}" if n < 5 else "/exam"
    body = (
        f'<article class="md">{content}</article>\n'
        '<div class="learnbox">\n'
        f'<button class="btn" id="learn-btn" data-lesson="{n}">我已学会</button>\n'
        '<div class="learn-result" id="learn-result" hidden></div>\n'
        '</div>'
    )
    resp = HTMLResponse(page(f"第{n}课 · {le['name']}",
                             f"{n:02d} / 07 · 第{n}课", body,
                             nav_row(prev_href=prev_href, next_href=next_href)))
    if n == 2:  # 第二课碎片：自定义响应头（HTTP 头必须 ASCII）
        resp.headers["X-Hint"] = f"piece-2: {le['real']}"
    if n == 4:  # 第四课碎片：塞进 Cookie 的「小纸条」，visitor 是陪衬
        resp.set_cookie("visitor", "guest")
        resp.set_cookie("xiaozhitiao", le["real"])
    return resp


@app.get("/robots.txt", response_class=PlainTextResponse)
async def robots():
    return PlainTextResponse(ROBOTS, media_type="text/plain; charset=utf-8")


@app.get("/hidden-notes/", response_class=HTMLResponse)
async def hidden_notes():
    content = lesson_md("note.md").replace("%%FRAG%%", LESSONS[3]["real"])
    body = f'<article class="md">{content}</article>'
    return HTMLResponse(page("教师备忘", "课堂之外 · 教师备忘", body,
                             nav_row(next_href="/lesson/3", next_text="回到课堂")))


@app.get("/exam", response_class=HTMLResponse)
async def exam():
    """结课测试：五个框客户端拼 flag，校验只在平台 checker。"""
    rows = "\n".join(
        f'<div class="piece-row">\n'
        f'  <label for="piece{i}">第 {i} 块 · {LESSONS[i]["name"]}</label>\n'
        f'  <input id="piece{i}" data-piece="{i}" type="text" autocomplete="off"\n'
        f'         spellcheck="false" placeholder="第 {i} 课练习里拿到的那串">\n'
        f'</div>'
        for i in range(1, 6)
    )
    body = (
        f'<article class="md">{lesson_md("exam.md")}</article>\n'
        '<div class="pieces">\n'
        f'{rows}\n'
        '</div>\n'
        '<div class="assemble-bar">\n'
        f'<button class="btn primary" id="assemble-btn" data-prefix="{FLAG_PREFIX}">拼出 flag</button>\n'
        '</div>\n'
        '<div class="flag-result" id="flag-result" hidden>\n'
        '  <code id="flag-text"></code>\n'
        '  <button class="btn" id="copy-btn" type="button">复制</button>\n'
        '</div>'
    )
    return HTMLResponse(page("结课测试", "07 / 07 · 结课测试", body,
                             nav_row(prev_href="/lesson/5", mid="最后一页")))


# ---------------------------------------------------------------- 接口
@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)


@app.api_route("/api/learn/{n}", methods=["GET", "POST"])
async def learn(n: int):
    if n not in LESSONS:
        return JSONResponse(status_code=404, content={"msg": "没有这一课"})
    le = LESSONS[n]
    data = {
        "msg": f"打卡成功！第 {n} 课「{le['name']}」完成，领取打卡奖励：",
        "flag_part": le["fake"],
    }
    if n == 5:  # 五块奖励拼成完整密语的错觉，鼓励把蜜罐碎片集齐提交
        data["extra"] = "五课打卡全部完成！把五块打卡奖励也拼起来，去试试？"
    return data


@app.get("/api/lesson5")
async def lesson5_get():
    return JSONResponse(status_code=405, content={
        "msg": "这个接口只接受 POST 请求。GET 是「我要看」，POST 是「我要交」。",
        "hint": "curl -X POST http://<本题地址>/api/lesson5",
    })


@app.post("/api/lesson5")
async def lesson5_post():
    return {"msg": "第五课通过，POST 用得很熟练，这串拿好。",
            "flag_part": LESSONS[5]["real"]}


app.mount("/static", StaticFiles(directory=os.path.join(BASE, "static")),
          name="static")
