# web_antshell —— 出题人文档

> 玩家不可见本文档。Web 入门题：备份泄漏引出一句话木马，用 WebShell 管理工具
>（题面推荐中国蚁剑）连接后读 `/flag`。

## 设计

```
首页维护公告（robots.txt 同样指向 /backup/）
        │ 下载 antcloud_backup.zip
        ▼
源码四件套：index.php / config.php / ant.php / robots.txt
        │ config.php 的 TODO 注释点名 ant.php
        ▼
ant.php：经典一句话 eval($_POST['ant'])，连接密码 ant
        │ 蚁剑「添加数据」（URL /ant.php，密码 ant，类型 PHP）
        ▼
虚拟终端 cat /flag（或文件管理器看 /flag）→ hctf{...}
```

入门教学点三个：备份泄漏找源码、认识一句话木马（GET 访问只报
`Undefined array key` 警告、连接密码即参数名，POST 才干活）、WebShell 管理
工具的基本操作（蚁剑添加数据 / 虚拟终端 / 文件管理器）。一句话不挑工具：
菜刀、哥斯拉（PHP EVAL 模式）、直接 curl POST 均可行，蚁剑只是题面推荐路径。

## 行为表

| 请求 | 表现 |
|---|---|
| `GET /`、`GET /robots.txt` | 站点页面 / robots（公告与 Disallow 指向 /backup/） |
| `GET /backup/antcloud_backup.zip` | 下载源码备份包（四文件，与部署一致） |
| `GET /ant.php` | 200 + `Warning: Undefined array key "ant"`（PHP 8 中 eval(null) 静默无操作；参数名即连接密码，报错即泄露） |
| `POST /ant.php`（密码参数 `ant`，值为任意 PHP 代码） | `eval` 执行，蚁剑正常回显 |

## 背景知识：蚁剑连上来时发了什么

蚁剑默认配置（PHP 类型 / default 编码器）把**整段 PHP 代码明文**放进连接密码
参数：固定头部 `@ini_set("display_errors", "0");@set_time_limit(0);`、
open_basedir 探测、`asenc/asoutput` 回显函数、`try/catch` 包裹的模板代码，
服务端 eval 后在随机 tag 之间回显数据（依据：蚁剑源码 source/core/php/index.js
的 complete()，release 2.1.16 与 master 逐字节一致）。writeup/exp.py 即按此
结构手搓请求，不开蚁剑复现完整利用链。

## Flag 约定（HCTF-2026 全场统一）

- 真 flag：`hctf{}` 包裹，**动态**——ret2shell 平台启动容器时注入 `FLAG` 环境变量，
  `entrypoint.sh` 将其写入 `/flag`；未注入时回退默认 `hctf{AntSword_0n1y}`
  （保持格式，静态部署可用）。
- 本题无蜜罐 / 假 flag，不使用 `fflag{}`。

## 黑盒

不发布源码附件（`attachment/` 缺省，按仓库惯例接受 warning）；选手仅有线上靶机地址，
备份包即题内自带的"源码发放口"。

## 部署

```bash
docker build -t web_antshell ./src
docker run -d -p 8080:80 -e FLAG="hctf{xxx}" web_antshell
```

运行时：`php:8.3-cli-alpine` + PHP 内置服务器（`PHP_CLI_SERVER_WORKERS=8`），
绑定 `0.0.0.0:80`。备份 zip 由 Dockerfile 构建期用 `zip` 命令现场打包
（官方 php:cli-alpine 不带 zip 扩展），与部署文件一一对应，不存在二次同步问题。

## 出题人配置点（共 2 处）

1. **默认 flag** — `src/entrypoint.sh` 的 `FLAG` 回退值。
2. **备份包文件清单** — `src/Dockerfile` 的 `zip -q backup/antcloud_backup.zip ...`
   文件列表（html 目录增删文件需同步）。

## 验证记录

neko 虚机（192.168.140.134）docker 实测：

- `docker build` + `docker run -e FLAG='hctf{...}'` 通过；
- 行为符合上表：页面/robots/zip 正常，GET ant.php 仅报 Undefined array key 警告，
  POST 任意 PHP 代码即执行（裸 payload 与蚁剑同构 payload 均放行）；
- `writeup/exp.py`（手搓蚁剑默认流量）取回注入 flag，闭环。
