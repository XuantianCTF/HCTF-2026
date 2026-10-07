# web_hidden_api —— 出题人文档（玩家不可见）

> Web 方向第三道热身题，考 **前端源码审计 + 隐藏接口**。相比前两题，
> 这题要求选手从"看"进阶到"读"：读懂 `app.js` 里的调试后门，解出 base64
> key，再自己构造请求去打隐藏 API。目的是让新手建立"前端即源码、接口可被
> 直接调用"的意识。

## 一、题目定位

| 项 | 值 |
|---|---|
| 分类 | Web |
| 难度 | 入门 |
| 技术栈 | Python 3 标准库 `http.server`（`python:3.12-alpine`） |
| 主要考点 | 浏览器开发者工具、前端 JS 审计、隐藏 API、base64 解码 |
| flag | `HCTF{...}`，平台注入 `FLAG` 环境变量 |
| 附件 | 无（线上靶机） |

## 二、环境架构

`src/server.py` 监听 `8082`，路由如下：

| 路径 | 方法 | 行为 |
|---|---|---|
| `/` | GET | 登录页（含"看脚本"提示） |
| `/static/app.js` | GET | 前端逻辑，泄露调试接口与 base64 key |
| `/api/v2/login` | POST | 永远返回"用户名或密码错误" |
| `/api/v2/backup?key=...` | GET | key 正确返回 flag，否则 403 |
| 其他 | * | 404 |

`app.js` 中的 `atob("bGV0bWVpbl8yMDI2")` 解码为 `letmein_2026`，
与 `server.py` 的 `DEBUG_KEY` 常量一致。

## 三、flag 约定

- 真 flag：`HCTF{...}`，**动态**，由 ret2shell 平台注入 `FLAG` 环境变量。
- 未注入时回退 `HCTF{j4v4scr1pt_1s_publ1c}`。
- 本题**无蜜罐 / 假 flag**。

## 四、出题人配置点

1. **flag**：无需改源码，部署时注入 `FLAG` 环境变量。
2. **端口**：`server.py` 读 `PORT` 环境变量，默认 `8082`。
3. **调试 key**：`server.py` 的 `DEBUG_KEY` 与 `app.js` 的 base64 需同步修改。
   若改 key，重新生成 base64 后替换 `atob(...)` 里的字符串即可。
4. **前端文案**：`src/index.html`、`src/app.js`。

## 五、预期解法

1. 登录失败，`F12` → Sources / Network，发现 `/static/app.js`。
2. 阅读 JS，发现注释里的调试后门与 `atob("bGV0bWVpbl8yMDI2")`。
3. `base64 -d` 解出 `letmein_2026`。
4. 请求 `GET /api/v2/backup?key=letmein_2026`，响应 JSON 的 `flag` 字段即答案。
5. 考点：前端审计、隐藏接口、base64 编码不是加密。

## 六、验收

```bash
docker build -t web_hidden_api ./src
docker run -d --rm -p 8082:8082 -e FLAG='HCTF{demo_hidden_api}' web_hidden_api
python3 writeup/exp.py http://127.0.0.1:8082
# 期望输出：HCTF{demo_hidden_api}
```

`exp.py` 为 PoC：抓取 `/static/app.js` → 正则取 `atob("...")` → base64 解码 →
请求隐藏接口 → 打印 flag。

## 七、防非预期

- flag 只由 `/api/v2/backup` 且 key 正确时返回；`/api/v2/login` 永不成功。
- 不存在其他泄露 flag 的路径。
- key 写在公开前端里本就是漏洞设计，属题目预期；base64 仅增加一层"需要动手解码"
  的门槛，防止无脑复制粘贴。
