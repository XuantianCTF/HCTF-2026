# web_antshell

- **分类**：Web
- **难度**：简单（入门）
- **题型**：源码暴露 + webshell 连接（一句话木马）

## 题面

打开就是一屏 PHP 源码——离职的运维小哥留下的"维护接口"。

看懂它，连上它，flag 就在服务器的文件系统里。

## 部署

```bash
docker build -t web_antshell ./src
docker run -d -p 8080:80 -e FLAG="hctf{xxx}" web_antshell
```
