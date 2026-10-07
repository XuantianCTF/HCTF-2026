# web_view_source

- **分类**：Web
- **难度**：入门
- **题型**：查看网页源代码（HTML 注释）
- **附件**：无

## 题面

欢迎来到 HCTF 2026 的第一道 Web 热身题。

flag 就藏在这个页面里，但无论你怎么看，页面上都不会显示它。

浏览器能把整份"源代码"都发到你手里，学会查看它，是每个 Web 选手的第一步。

拿到 flag 提交即可。

## 提示

1. 页面上看到的文字，只是源代码的一部分。
2. 试试浏览器快捷键：`Ctrl+U` / `Cmd+Option+U`，或者 `F12`。
3. 注释不会显示在页面上，但会随响应发给浏览器。

## 部署

```bash
docker build -t web_view_source ./src
docker run -d -p 8080:8080 -e FLAG="HCTF{xxx}" web_view_source
```

服务监听容器 `8080` 端口，flag 由平台通过 `FLAG` 环境变量注入。
