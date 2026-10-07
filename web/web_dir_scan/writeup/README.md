# web_dir_scan —— 出题人文档（玩家不可见）

> Web 方向第二道热身题，考 **信息收集 / 目录扫描**。核心引导点是
> `robots.txt`：它既是真实存在的爬虫约定，也是新手最该养成的第一个排查习惯。
> 隐藏目录名刻意取得怪异，逼选手先看 `robots.txt` 或用字典，而不是凭直觉猜。

## 一、题目定位

| 项 | 值 |
|---|---|
| 分类 | Web |
| 难度 | 入门 |
| 技术栈 | Python 3 标准库 `http.server`（`python:3.12-alpine`） |
| 主要考点 | `robots.txt` 信息泄露、隐藏目录访问、状态码观察（403 vs 404） |
| flag | `HCTF{...}`，平台注入 `FLAG` 环境变量 |
| 附件 | 无（线上靶机） |

## 二、环境架构

`src/server.py` 是单文件路由服务，监听 `8081`，全部路径在代码里显式声明：

| 路径 | 状态码 | 内容 |
|---|---|---|
| `/` | 200 | 首页 + 目录扫描小课堂 |
| `/robots.txt` | 200 | `Disallow: /s3cr3t_r00m/`、`/backup/` |
| `/s3cr3t_r00m/` | 200 | 目录列表（`readme.txt`、`flag.txt`） |
| `/s3cr3t_r00m/flag.txt` | 200 | flag 明文 |
| `/s3cr3t_r00m/readme.txt` | 200 | 提示提交 flag |
| `/backup/` | 403 | 诱饵：存在但禁止访问 |
| 其他 | 404 | 文案暗示去翻 robots.txt |

## 三、flag 约定

- 真 flag：`HCTF{...}`，**动态**，由 ret2shell 平台注入 `FLAG` 环境变量。
- 未注入时回退 `HCTF{rrrobots_txt_l34ds_th3_w4y}`。
- 本题**无蜜罐 / 假 flag**；`/backup/` 是纯诱饵，不含任何 flag。

## 四、出题人配置点

1. **flag**：无需改源码，部署时注入 `FLAG` 环境变量。
2. **端口**：`server.py` 读 `PORT` 环境变量，默认 `8081`。
3. **隐藏目录名 / robots 内容**：`src/server.py` 顶部常量，可自由改。
4. **诱饵目录**：`/backup/` 返回 403，可按需增删。

## 五、预期解法

1. 首页无有效链接；`curl /robots.txt` 发现 `Disallow: /s3cr3t_r00m/`。
2. 访问 `/s3cr3t_r00m/` 得到目录列表。
3. 读取 `/s3cr3t_r00m/flag.txt` 得到 flag。
4. 等价路径：用 dirsearch / ffuf / gobuster 扫出 `/s3cr3t_r00m/`。
5. 考点：robots.txt 泄露、目录扫描、403/404 区分。

## 六、验收

```bash
docker build -t web_dir_scan ./src
docker run -d --rm -p 8081:8081 -e FLAG='HCTF{demo_dir_scan}' web_dir_scan
python3 writeup/exp.py http://127.0.0.1:8081
# 期望输出：HCTF{demo_dir_scan}
```

`exp.py` 为 PoC：依次请求 `/robots.txt` 解析出 `Disallow` 路径，进入目录，
再读取 `flag.txt` 并打印。

## 七、防非预期

- flag 只存在于 `/s3cr3t_r00m/flag.txt`，没有其他路径会返回它。
- 首页、404、403 页面均不含 flag。
- 若选手直接猜测到隐藏目录（运气解）也可完成，属可接受；`robots.txt`
  仍是最短路径。
