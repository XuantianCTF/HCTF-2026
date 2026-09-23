# pathconfusion 解题过程

## 0x00 入口侦察

题面明说"登录页不是让你登进去的"，那就先做信息搜集。`robots.txt` 直接给出两条线索：

```
User-agent: *
Disallow: /doc.html
Disallow: /sc/api/
```

访问 `/doc.html`，网关 403；`/sc/api/` 下能摸到一批业务接口（组织架构、用户、应用列表），但都要会话。重点回到那个被 403 的内部文档上。

## 0x01 朴素穿越为什么不行

第一反应是路径穿越：`/sc/../doc.html`——仍然 403。

原因：Nginx 在做 location 匹配**之前**会自己对 URI 做归一化（折叠 `./`、`../`），`/sc/../doc.html` 折叠后就是 `/doc.html`，精确命中网关上的 `location = /doc.html { return 403; }`。穿越发生在网关自己的规范化里，等于自投罗网。

## 0x02 两层解析器的缝隙

再想网关的转发面：`/sc/` 前缀的 location 是"原样转发"——`proxy_pass ... $request_uri` 带的是**未经归一化的原始请求行**。也就是说，只要一个 URI 能在 Nginx 的归一化下"不像 `/doc.html`"，又能骗过 `/sc/` 前缀匹配，后端就会收到原始串。

缺的最后一块拼图是老后端（Tomcat 系）的解析语义：**每个路径段中 `;` 之后的内容是路径参数（path parameter），路由前先剥离**。

于是 `/sc/..;/doc.html` 在两层的遭遇完全不同：

| 层 | 看到的路径 | 处理 |
|---|---|---|
| Nginx | `/sc/..;/doc.html` | `..;` 不是合法点段不折叠；不等于 `/doc.html` 不触发拦截；`/sc/` 前缀命中，`$request_uri` 原样转发 |
| 后端 | `/sc/..;/doc.html` | 剥 `;` 参数 → `/sc/../doc.html` → 点段归一化 → `/doc.html`，返回文档 |

## 0x03 拿 flag

```bash
curl --path-as-is 'http://HOST:58000/sc/..;/doc.html'
```

注意 `--path-as-is`：不加的话 curl 自己会先折叠 `../`。页面"开发调试记录"一段即 `hctf{...}`。

顺带一提，doc.html 里的接口文档列出了平台全部端点，还附了一段联调抓包的登录密文——对同环境的后续题目是有价值的线索。
