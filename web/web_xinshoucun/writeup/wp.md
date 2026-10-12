# web_xinshoucun Writeup

教学题：每关先教后考，解法就是「用本关刚教的知识」。以下按通关顺序。

## 第一关 · 看见（口令 eyes-open → EYES）

按 Ctrl+U 看源码，HTML 注释里老兵留言：告示牌是 JS 动态挂的、罩着 display:none，
源码里没有，去 Elements 找。F12 → Elements → Ctrl+F 搜 `notice-board`，
隐藏 `div` 的文本里就是口令 `eyes-open`（也可以去 Network 面板读 `village.js` 源码，殊途同归）。
提交口令领装备词 EYES。

要点：**「查看源代码」是服务器发的原始 HTML；Elements 是浏览器跑完 JS 的现场**——
JS 动态插入的节点只在后者里。

## 第二关 · 对话（口令 say-hello → VOICE）

`messenger.php` 只认两张「名片」，且缺什么报什么（三态渐进报错即引导）：

1. 裸访问：名片不像信使 → UA 必须是 `RookieCourier/1.0`
2. UA 对了：介绍信呢 → Referer 必须是 `https://elders.village.gov/`

浏览器不方便改这两个头，用页面教的 curl 一条命令带上：

```bash
curl -A "RookieCourier/1.0" -H "Referer: https://elders.village.gov/" \
     http://HOST:58000/messenger.php
```

回执口令 `say-hello`，提交领 VOICE。

## 第三关 · 改造（口令 smith-hand → HANDS）

购买表单的 `price` 是 hidden 字段（100 金币 > 钱包 10）。前端「验钞机」
（onsubmit 的 JS 校验）只是门帘，三条路任选：

- F12 → Elements 双击改 `price` 的 value 再提交
- 或干脆绕开页面，用第二课的 curl 直接递单子：

```bash
curl -X POST -d "item=sword-blueprint&price=10" http://HOST:58000/forge.php
```

服务端只验 `1 ≤ price ≤ 10`（防零元购/负数），10 金币成交。
返回 Base64 密文，`atob("...")` 解出 `smith-hand`，提交领 HANDS。

## 第四关 · 探索（口令 trail-blazer → MAP）

经典三连：

1. `GET /robots.txt` → `Disallow: /map-v2.php.bak`
2. `GET /map-v2.php.bak` → 不被当 PHP 执行，源码原样吐出，
   注释里 `$INTERNAL_KEY = 'hunter2026'` 及接口用法 `GET /supply.php?key=<KEY>`
3. `GET /supply.php?key=hunter2026` → 口令 `trail-blazer`，提交领 MAP

「禁止入内」的牌子就是路标；密钥写进备份注释的那一刻，锁就等于没了。

## 第五关 · 出剑（口令 first-blood → SWORD）

用下发账号 `rookie / rookie123` 登录村公所（领 PHPSESSID 手环）。

- `profile.php` 是**正面教材**：改 `uid=1000` 查村长会被拒（服务端校验 uid == 会话身份）
- 但档案页里有「查看我的荣誉证书」链接，长得是 `cert.php?uid=1001`——
  证书处**没接身份核验**（IDOR）：

```
GET /cert.php?uid=1000   （村长档案号，村志页面明示）
```

村长证书的「荣誉口令」是 Base64 存档 `Zmlyc3QtYmxvb2Q=`，解码得 `first-blood`，
提交领 SWORD。

## 毕业门 → flag

五个装备词 `EYES / VOICE / HANDS / MAP / SWORD` 依次填入毕业门，
门后石碑发放部署时注入的 `FLAG`（回退默认 `hctf{EYES_VOICE_HANDS_MAP_SWORD}`）。

## 修复建议（每关对应的真实世界姿势）

| 关 | 漏洞面 | 修法 |
|---|---|---|
| 1 | 注释泄密、隐藏即安全 | 生产环境删调试注释；敏感信息永不进前端 |
| 2 | 仅凭请求头做访问控制 | 请求头可伪造，鉴权走服务端会话 |
| 3 | 信任客户端价格 | 金额等关键字段一律服务端重算，不信表单值 |
| 4 | 备份/密钥泄露 | 部署产物进版本管理、服务器不落 .bak；密钥用环境变量/密管 |
| 5 | IDOR | 每个接口都做对象级鉴权（uid 归属校验），不只是「登录了没」 |
