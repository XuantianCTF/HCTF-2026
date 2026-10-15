# web_growcode writeup

## 概览

- **考点**：动态源码审计意识、黑名单绕过（通配符）、命令分隔符与空格过滤、变量覆盖（`extract($_POST)`）、GET/POST 复合请求
- **难度**：入门
- **完整解题过程**：[wp.md](wp.md)
- **利用链 PoC**：[exp.py](exp.py)

## 快速复现

```bash
docker build -t web_growcode ./src
docker run -d -p 58002:80 -e FLAG="hctf{test_grow}" web_growcode
python exp.py http://127.0.0.1:58002
```

## 机制说明（出题人视角）

页面按"当前请求达到的最高层级"渲染源码：层级配置数组中每层包含"展示源码文本"与"触发判定闭包"，触发只看本次请求的参数组合（无状态、无会话）。被展示的过滤规则与真实执行的过滤共用同一份常量与文案，选手审计到的就是真实生效的规则——"生长"只是按层揭示。

四层触发条件：

| 层 | 触发条件 | 生效过滤 |
|---|---|---|
| L1 | 默认 | 无 |
| L2 | cmd 命中敏感词黑名单 | 黑名单 |
| L3 | cmd 含 `\|;&><` | 黑名单 + 去空白 + 限长 16 |
| L4 | 请求带 POST 体，或 cmd 含 `` $ ` { `` | 以上全部 + extract 重校验 + 通关分支 |

## 沙箱设计（命令执行题的安全底线）

flag 在环境变量中，命令执行题的最大泄露路径是 `/proc/*/environ`，防护组合：

1. PHP 主进程 root 运行，选手命令统一 `timeout 3 su -s /bin/sh www-data -c <cmd>` 降权执行——www-data 对 root 进程的 `/proc/*/environ` 无读取权限（ptrace 访问检查）；
2. 脚本启动即 `putenv('FLAG')` 清除进程环境，降权后的子进程环境变量里没有 FLAG，`env`、`/proc/self/environ`（自身）均拿不到；
3. `chmod 600 /app/index.php`，降权 shell 无法读取引擎源码（否则 `paste index.php` 这类未拉黑读取器直接毕业）；
4. `disable_functions` 禁用 PHP 文件/目录/网络函数 + `open_basedir=/app`；
5. 诱饵 `/flag`（644，可读）内容为假 flag，拦截住了"读文件拿 flag"的期望，同时指引真实方向。

## 踩坑记录

- **busybox ash 的 glob 规则**：参数与绝对路径词会展开（`/bin/ca? /fla?` 可用），但裸命令词（`ca? /fla?` 报 not found）与重定向目标（`cat</fla?` 报 can't open）都不做 glob——免空格重定向绕过在 alpine 上不成立，L3 是纯墙层，设计上把玩家推向 `${IFS}`/POST 晋级 L4。
- **extract 守卫**：引擎最初有 `if ($cmd !== '')` 外层守卫，导致"POST 直接带 `cmd=s&auth=admin`、GET 不带 cmd"时整个通关分支被跳过。展示代码的语义是 v2/v3 检查在空串上自然放行、v4 的 extract 无条件执行，引擎逐行对齐后该路径才通。
- **PHP_CLI_SERVER_WORKERS**：内置服务器默认单进程，必须用环境变量开 worker（`-d` 方式无效）。
- **源码 600 是必须的**：黑名单拉不完所有读取器（paste、xargs、while read……），文件系统权限才是根治；同时 "php" 一词在黑名单里恰好让 `index.php` 这个词本身被拦。
