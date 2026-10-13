# web_antshell —— 出题人文档

> 玩家不可见本文档。Web 入门题：单文件 PHP 页自暴露源码，源码里就是
> 一句话木马；用 WebShell 管理工具连接后读 `/flag`。

## 设计

```
GET /（index.php 整个站点就这一个文件）
        │ highlight_file(__FILE__) 直接回显自身源码
        ▼
源码 = 题面：@eval($_POST['HCTF'])，连接密码 HCTF
        │ WebShell 管理工具「添加数据」（URL /，密码 HCTF，类型 PHP）
        ▼
虚拟终端 cat /flag（或文件管理器看 /flag）→ hctf{...}
```

极简三行：`highlight_file` 负责"源码暴露"（题面即源码，零附加信息），
`@eval` 负责一句话木马。入门教学点：认识一句话木马与连接密码即参数名、
WebShell 管理工具的基本操作（添加数据 / 虚拟终端 / 文件管理器）。
一句话不挑工具：任意 WebShell 管理器或直接 curl POST 均可行。

## 行为表

| 请求 | 表现 |
|---|---|
| `GET /` | 200，回显 index.php 自身源码（highlight_file 高亮输出） |
| `POST /`（密码参数 `HCTF`，值为任意 PHP 代码） | 源码回显 + `eval` 执行输出；前置的源码输出不影响管理工具提取执行结果 |

## Flag 约定（HCTF-2026 全场统一）

- 真 flag：`hctf{}` 包裹，**动态**——ret2shell 平台启动容器时注入 `FLAG` 环境变量，
  `entrypoint.sh` 将其写入 `/flag`；未注入时回退默认 `hctf{W3lc0m3_T0_Websh3ll}`
  （保持格式，静态部署可用）。
- 本题无蜜罐 / 假 flag，不使用 `fflag{}`。

## 黑盒

不发布源码附件（`attachment/` 缺省，按仓库惯例接受 warning）；选手仅有线上靶机地址，
页面自身即"源码发放口"。

## 部署

```bash
docker build -t web_antshell ./src
docker run -d -p 8080:80 -e FLAG="hctf{xxx}" web_antshell
```

运行时：`php:8.3-cli-alpine` + PHP 内置服务器（`PHP_CLI_SERVER_WORKERS=8`），
绑定 `0.0.0.0:80`，webroot 仅 index.php 一个文件。

## 出题人配置点（共 1 处）

1. **默认 flag** — `src/entrypoint.sh` 的 `FLAG` 回退值。

## 验证记录

neko 虚机（192.168.140.134）docker 实测：

- `docker build` + `docker run -e FLAG='hctf{...}'` 通过；
- 行为符合上表：GET / 回显自身源码；POST 任意 PHP 代码即执行
  （裸 curl payload 与 WebShell 管理器流量均放行）；
- `writeup/exp.py` 取回注入 flag，闭环。
