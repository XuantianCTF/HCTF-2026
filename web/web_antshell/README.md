# web_antshell

- **分类**：Web
- **难度**：简单（入门）
- **题型**：备份泄漏 + webshell 连接（一句话木马）

## 题面

蚂蚁云运维平台升级维护中，站点已回滚至备份版本。

听说离职的运维小哥临走前在站里留了个后门。找到它，连上去，flag 就在服务器的文件系统里。

（预期解法工具：中国蚁剑 AntSword；其他 WebShell 管理工具同样可行。）

## 部署

```bash
docker build -t web_antshell ./src
docker run -d -p 8080:80 -e FLAG="hctf{xxx}" web_antshell
```
