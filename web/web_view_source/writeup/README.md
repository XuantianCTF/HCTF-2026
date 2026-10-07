# web_view_source —— 出题人文档（玩家不可见）

> Web 方向第一道热身题，只考一件事：**会看网页源代码**。
> 页面用"小课堂"的形式手把手引导选手按 `Ctrl+U` / `F12`，flag 放在
> 响应 HTML 的注释里，页面上不渲染，但不做任何加密或隐藏。

## 一、题目定位

| 项 | 值 |
|---|---|
| 分类 | Web |
| 难度 | 入门 |
| 技术栈 | Python 3 标准库 `http.server`（`python:3.12-alpine`） |
| 主要考点 | 查看网页源代码 / 浏览器开发者工具 / HTML 注释 |
| flag | `HCTF{...}`，平台注入 `FLAG` 环境变量 |
| 附件 | 无（线上靶机） |

## 二、环境架构

`src/server.py` 是单文件 HTTP 服务，监听 `8080`。读取同目录的
`index.html` 模板，把占位符 `{{FLAG}}` 替换成运行时 `FLAG` 环境变量后返回，
因此 flag 不会以明文写死在仓库里。

```python
FLAG = os.environ.get('FLAG', 'HCTF{v13w_s0urc3_1s_4ll_y0u_n33d}')
html = f.read().replace('{{FLAG}}', FLAG)
```

## 三、flag 约定

- 真 flag：`HCTF{...}`，**动态**，由 ret2shell 平台注入 `FLAG` 环境变量。
- 未注入时回退演示值 `HCTF{v13w_s0urc3_1s_4ll_y0u_n33d}`，方便本地直接跑。
- 本题**无蜜罐 / 假 flag**。

## 四、出题人配置点

1. **flag**：无需改源码，部署时注入 `FLAG` 环境变量。
2. **端口**：`server.py` 读 `PORT` 环境变量，默认 `8080`。
3. **页面文案 / 提示**：`src/index.html`，其中注释同样可自由改动。

## 五、预期解法

1. 打开页面，看到"查看源代码"小课堂。
2. `Ctrl+U` / `F12`（或 `curl`）拿到 HTML 源码。
3. 底部注释里 `FLAG: HCTF{...}` 即答案。
4. 考点：把"页面上看到的"与"服务器实际发来的"区分开。

## 六、验收

```bash
docker build -t web_view_source ./src
docker run -d --rm -p 8080:8080 -e FLAG='HCTF{demo_view_source}' web_view_source
python3 writeup/exp.py http://127.0.0.1:8080
# 期望输出：HCTF{demo_view_source}
```

`exp.py` 为 PoC：请求首页，从 HTML 注释里正则提取 `HCTF{...}` 并打印。

## 七、防非预期

- 页面在浏览器中**完全不显示** flag，不看源码拿不到。
- 无其他接口、无目录可扫，唯一入口就是首页源码。
