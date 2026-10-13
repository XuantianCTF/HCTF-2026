# web_xinshoucun

- **分类**：Web
- **难度**：入门
- **题型**：教考一体 · 五小关联动（源码/DevTools → HTTP 请求头 → 表单篡改与编码 → 信息收集 → 越权）
- **附件**：无

## 题面

「WEB 新手村」——RPG 包装的教学型题目：五位导师各守一关，每关「教学 → 实操 → 口令 → 领装备」，
讲的全是本关要用的知识，不考课外内容。五关分别拿到装备词
`EYES / VOICE / HANDS / MAP / SWORD`，在毕业门依次归位，门后石碑即是 flag。

- 目的是**教**：每关页面内嵌教学区 + 两层折叠提示（第二层给可直接复制的命令），看提示通关也算学会
- 口令全部在服务端校验，view-source 拿不到任何答案；但每一步都在玩家「刚学会的能力圈」内
- 各关卡地址带随机后缀且只在通关奖励页发放，跳关无门（教学题，不做强防）

## 提示

1. 第一关：口令不在页面里、也不在「查看源代码」里——它在浏览器跑完 JS 之后的实时 DOM 里
2. 第三关：门口的「验钞机」只是前端 JS；柜台认的是订单上写的价格，而订单要先经过你的电脑
3. 第五关：档案处管得严（正面教材，别死磕），证书处是新文员值班——同一个网站，柜员松紧不一

## 部署

```bash
docker build -t xinshoucun ./src
docker run -d -p 58000:80 -e FLAG="hctf{xxx}" xinshoucun
```

- 服务监听容器内 `0.0.0.0:80`（`php:8.3-cli-alpine` + PHP 内置服务器，
  `PHP_CLI_SERVER_WORKERS=8`），宿主端口 `58000`
- **动态 flag**：平台向容器注入 `FLAG` 环境变量，毕业门（五装备词验证通过后）
  原样发放；未注入时使用代码内回退值 `hctf{EYES_VOICE_HANDS_MAP_SWORD}`（保持 `hctf{}` 格式）
- 无数据库、无外部依赖，纯 PHP 单容器；session 用 PHP 内置文件存储
- 五个装备词是通关凭证不是 flag 本体——判分只认毕业门发放的注入值

## 关卡与考点速查（出题人向）

| 关卡 | 文件 | 考点 | 口令 | 装备词 |
|---|---|---|---|---|
| 1 看见 | `s1-look-f3a9.php` | Ctrl+U / HTML 注释 / Elements / display:none / JS 动态 DOM | `eyes-open` | EYES |
| 2 对话 | `s2-speak-7c21.php` | HTTP 报文 / UA / Referer / curl（`messenger.php` 三态渐进报错） | `say-hello` | VOICE |
| 3 改造 | `s3-forge-b55d.php` | hidden 字段 / 前端校验绕过 / Base64（`forge.php` 验 1≤price≤10） | `smith-hand` | HANDS |
| 4 探索 | `s4-explore-e842.php` | robots.txt / `.bak` 备份泄露 / 源码泄露（`supply.php?key=`） | `trail-blazer` | MAP |
| 5 出剑 | `s5-hit-d19c.php` | 登录会话 / IDOR（`profile.php` 严 vs `cert.php?uid=1000` 松） | `first-blood` | SWORD |
| 毕业门 | `graduate-a67f.php` | 五装备词归位 → 发放注入的 `FLAG` | — | flag |
