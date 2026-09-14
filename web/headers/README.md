# headers

出题人：lengkur

一个用于信息搜集方向的 Web 题：

- 访问 `/` 时先跳转到 `/gateway.php`
- `/gateway.php` 在响应头中返回 `X-CTF-Flag`
- 随后再次跳转到 `/final.php`
- 最终页面只给出弱提示，选手需要抓跳转链里的响应头

本题默认从环境变量 `GZCTF_FLAG` 读取 flag；未提供时使用演示值。

启动方式：

```bash
docker build -t web-headers .
docker run --rm -p 8080:80 -e GZCTF_FLAG='flag{test}' web-headers
```
