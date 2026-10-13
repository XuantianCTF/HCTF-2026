# web_antshell

- **分类**：Web
- **难度**：简单
- **题型**：备份泄漏 + webshell 连接（中国蚁剑）

## 题面

蚂蚁云运维平台升级维护中，站点已回滚至备份版本。

离职的运维小哥留了个后门，还放了话：这后门只认我的蚁剑，别的工具连上来，连个响都听不见。

## 部署

```bash
docker build -t web_antshell ./src
docker run -d -p 8080:80 -e FLAG="hctf{xxx}" web_antshell
```
