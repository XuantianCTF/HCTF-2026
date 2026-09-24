# headerauth 解题过程

## 0x00 整改之后，还剩什么

第三次来这个平台了。前两条路都试过：`/sc/..;/doc.html` 现在一律 404——后端把
老式路径解析层拆了；app.js 里那把私钥也换了齿，拿它解任何密文都过不了
PKCS1 padding。整改像模像样。

但 `robots.txt` 还是老样子：

```
User-agent: *
Disallow: /doc.html
Disallow: /sc/api/
```

`/doc.html` 死了，`/sc/api/` 还活着——禁区划给谁看，说明底下就有东西。

## 0x01 真开放的入口

题1 的 doc.html 接口表还在手上：`/sc/api/application/open/ssoLogin/`，备注
"单点登录跳转入口，302 并下发会话 Cookie"。本实例的 doc.html 已经摸不进去
了，但地图不需要再摸一遍。

直接 GET，果然 302，还顺手 `Set-Cookie: customsid=...`。路径里写着 open，
确实 open——一个不需要任何凭据就发会话的入口。

有会话 ≠ 有身份。拿它去接口表里的 `/sc/api/authc/users`，403「无权访问」：
会话过了，身份没过。那身份从哪来？

## 0x02 谁在替我说话

F12 打开，登录页只引一个业务 JS：`app.*.js`。拖下来 grep 一眼：

```
$ grep -o 'headers\.[a-z]*\.loginUser[A-Za-z]*' app.*.js | sort -u
e.headers.delete.loginUserId
e.headers.get.loginUserId
e.headers.post.loginUserId
...（loginUserOrgId 同款）
```

axios 拦截器在每次请求前，把 `loginUserId` / `loginUserOrgId` 两个头塞进请求——
**用户的身份是前端自己写在请求头里的**。登录成功后 sessionStorage 里有用户信息，
拦截器才有东西可塞；但后端只认头，不认头是怎么来的。手一挥就替我"说完了"。

管理员是哪位？`/sc/api/authc/orgs` 里 orgId=-1 叫「系统管理员」；userId
从 1 试起——`loginUserId: 1` + `loginUserOrgId: -1`，一发即中。

## 0x03 摘要与全量

带管理员头查列表，`?name=Neeco` 命中一条，userId=20258888。但列表只回 10 个
摘要字段，没有 flag。换详情接口 `/sc/api/authc/users/20258888`——54 个字段的
全量档案，`description` 里写着"插班生档案（涉密）。奖励核查通过后发放迎新系统
兑换码：`hctf{...}`"。

## 0x04 复盘

- 信任缝隙：网关假定后端会鉴权，后端假定网关已鉴权，中间没有人真的在看
- 请求头里的身份不是身份——凡是客户端可写、服务端当真的字段，都是后门
- 会话（customsid）与授权（loginUserId）混在两层各管一半，缝隙就在接缝处
