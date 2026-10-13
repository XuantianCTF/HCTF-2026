# web_antshell —— 出题人文档

> 玩家不可见本文档。Web 简单题：备份泄漏引出 webshell 源码，源码里写明
> 「只认中国蚁剑」的流量特征校验，用蚁剑默认配置连接后读 `/flag`。

## 设计

```
首页维护公告（robots.txt 同样指向 /backup/）
        │ 下载 antcloud_backup.zip
        ▼
源码四件套：index.php / config.php / ant.php / robots.txt
        │ config.php 的 TODO 注释点名 ant.php
        ▼
ant.php：POST 密码参数 ant，三重蚁剑流量特征校验，不过则 404
        │ 蚁剑默认配置连接（URL /ant.php，密码 ant，类型 PHP，编码器 default）
        ▼
虚拟终端 cat /flag（或文件管理器看 /flag）→ hctf{...}
```

考点：备份泄漏找到后门 + 认识蚁剑默认流量结构（前缀 `@ini_set("display_errors", ...)`、
open_basedir 探测、`asoutput()` 回显）。对工具党是一道标准蚁剑连接题；
源码在备份里白给，难点只在"看懂校验为什么只放行蚁剑"。

## 「只认蚁剑」的依据（源码级核实）

蚁剑 `source/core/php/index.js` 的 `complete()` 组装每次请求，`source/core/base.js`
的默认编码器 `default(pwd, data)` 原样下发：`data[pwd] = data['_']`，即**整段 PHP 明文
就是连接密码参数的值**，结构固定为：

```php
@ini_set("display_errors", "0");@set_time_limit(0);
if(!function_exists("get_magic_quotes_gpc")){...}
$opdir=@ini_get("open_basedir");if($opdir){...bypass...}
function asenc($out){return $out;};          // default 解码器
function asoutput(){...echo tag_s...tag_e...}
ob_start();try{<模板代码>;}catch(Exception $e){echo "ERROR://"...}
asoutput();die();
```

已核对 GitHub release `2.1.16` 与 master 该文件逐字节一致（2.1.15 同构），
默认配置全版本满足校验。ant.php 的校验取其中三个稳定特征：

| 校验 | 特征 | 来源 |
|---|---|---|
| 前缀 `strpos(...) === 0` | `@ini_set("display_errors"` | payload 固定开头 |
| 包含 | `open_basedir` | bypass 探测代码 |
| 包含 | `asoutput()` | 回显收尾函数 |

其他工具为何全灭：哥斯拉/冰蝎为加密流，菜刀模板结构不同，直接 `ant=system(...)` 的
裸 payload 更是连第一关都过不去——统一 404，与访问不存在路径的表现一致。

**不校验 UA**：蚁剑请求 UA 是 `random-fake-useragent` 随机浏览器 UA
（`modules/request.js`），无固定特征，不能作判定。

## Flag 约定（HCTF-2026 全场统一）

- 真 flag：`hctf{}` 包裹，**动态**——ret2shell 平台启动容器时注入 `FLAG` 环境变量，
  `entrypoint.sh` 将其写入 `/flag`；未注入时回退默认 `hctf{AntSword_0n1y}`
  （保持格式，静态部署可用）。
- 本题无蜜罐 / 假 flag，不使用 `fflag{}`。

## 行为表

| 请求 | 表现 |
|---|---|
| `GET /`、`GET /robots.txt` | 站点页面 / robots（公告与 Disallow 指向 /backup/） |
| `GET /backup/antcloud_backup.zip` | 下载源码备份包（四文件，与部署一致） |
| `GET /ant.php`（或任意非蚁剑 POST，含裸 `ant=system(...)`） | `404` + 站点风格 404 页 |
| 蚁剑默认配置 POST `/ant.php`（密码 `ant`） | 放行 `eval`，蚁剑正常回显 |

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
- 三态行为符合上表：普通 GET / 裸 POST 一律 404，蚁剑同构 payload 放行；
- `writeup/exp.py`（手搓蚁剑默认流量）取回注入 flag，闭环。
