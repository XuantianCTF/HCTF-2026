# leakedkey 解题过程

## 0x00 上一题的既视感

同一套统一身份认证平台，题面却提醒："上一题，你是不是漏看了一个很重要的东西"。

回忆 pathconfusion 的流程：`/sc/..;/doc.html` 绕过网关读到了内部接口文档
doc.html——那上面除了上一题的 flag，还有一段「开发调试记录」，提到管理员
测试账号的登录密文。当时只顾着交 flag 没多想，现在回过味来：素材就是它。

## 0x01 密文在哪

原样再进一次：`GET /sc/..;/doc.html`，200。

「开发调试记录」写着"密码密文如下，公钥存于本地"——可渲染出来的页面里
根本没有密文，只有一串 `fflag{...}`（正经 flag 是 `hctf{}` 前缀，这串对不上，
纪念品而已）。写着"如下"却看不见，那只剩一个地方：网页源代码。

view-source，密文果然躺在 HTML 注释里：

```html
<!-- <p><code id="ct">545dd8d6...（256 位 hex）...</code></p> -->
```

运维大概觉得注释掉就算"下线"了——注释只是不渲染，字节一个不少。

## 0x02 公钥加密的前端，藏不住私钥

"公钥存于本地"——本地能存哪？前端资产。登录页 view-source 只引了一个业务
JS：`app.*.js`，约 49 万字节的 webpack 打包产物。整个拖下来 grep：

```
$ grep -o 'public_exponent:"[0-9a-f]*"' app.*.js
public_exponent:"010001"
$ grep -o 'modulus:"[0-9a-f]*"' app.*.js
modulus:"009b127e...（256 位 hex）"
$ grep -o 'private_exponent:"[0-9a-f]*"' app.*.js
private_exponent:"0097cf2d...（256 位 hex）"
```

一个"公钥加密"的前端把 `private_exponent` 也打进了包——因为它运行时
真的要用私钥处理 token，索性整套硬编码。n、e、d 到齐，私钥等于白送。

## 0x03 一行 pow

```python
n, d, c = ..., ..., int(ct, 16)
m = pow(c, d, n)
b = m.to_bytes(128, "big")
plain = b[b.index(0, 2) + 1:]      # 去 PKCS1-v1_5 padding: 00 02 PS 00 M
```

管理员测试口令到手，就是本题 flag（`hctf{...}`）。

## 0x04 复盘

- 前端没有任何秘密可言：硬编码私钥 = 明文
- 注释不是删除
- 一条链上的题会互相递刀：上一题"顺手路过"的文档，是这一题的全部素材
