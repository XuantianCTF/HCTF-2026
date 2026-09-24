# leakedkey Writeup

## 漏洞点

1. **网关/后端解析差异（题1 同款，复用）**：`/doc.html` 被 nginx 网关 403，
   但 `/sc/` 前缀原样转发到后端，后端复刻 Tomcat 老式解析——先剥离路径参数
   （`;` 之后内容）再做点段归一化。于是 `GET /sc/..;/doc.html` 在网关眼里是
   `/sc/` 下的普通请求，到后端却归一化成 `/doc.html`，调试记录里的管理员
   登录密文（RSA/None/PKCS1-v1_5，1024 bit，hex）到手。
2. **前端泄露 RSA 私钥（本题考点）**：登录页 `/assets/js/app.*.js`
   （约 49 万字节，webpack 打包产物）硬编码了整套密钥常量：

   ```js
   TAG:"lyasp", public_exponent:"010001", modulus:"009b...", private_exponent:"97c..."
   ```

   "公钥加密"的前端却同时携带 `private_exponent`（d）——n、e、d 全在手上，
   密文 `m = pow(c, d, n)` 再去 PKCS1-v1_5 padding 即得明文。

注意：doc.html 调试记录里明摆着的 `fflag{...}` 是静态诱饵（占的是链上题1 的
flag 槽位），判分不收。

## 利用思路

1. 复用题1 手法：`GET /sc/..;/doc.html`，从「开发调试记录」的页面源码里
   抄下密文 hex（渲染页不可见，密文在 HTML 注释内）
2. 打开登录页，`view-source` 找到 app.js；grep 三个常量 `modulus` /
   `public_exponent` / `private_exponent`
3. RSA 解密：`m = pow(c, d, n)`，再按 PKCS1-v1_5 去 padding

## exp

```bash
python3 exp.py http://HOST:58000   # 自动绕网关取密文 + 提取私钥 + 解密
```

`exp.py` 无第三方依赖（纯 Python 实现 PKCS1-v1_5 unpad），解密结果即
`hctf{...}`（本环境动态注入的管理员测试口令）。

## 本实例在赛题链中的位置

三题链（pathconfusion → **leakedkey** → 题3）的题2 切片：保留题1 同款解析
差异作为密文获取通道；真 flag 由本容器 `FLAG` 环境变量在启动时加密进密文，
动态闭环在题内完成。题3 槽位为无害占位符（"已回收"）。
