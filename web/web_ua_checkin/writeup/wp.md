# web_ua_checkin 解题过程

题面：这份资料，为 iPhone 独占打造。

## 0x00 访问，被送去看视频

电脑浏览器打开靶机地址，瞬间被跳转到一个不相干的 bilibili 视频。用 curl 看响应头：

```
$ curl -I http://<靶机地址>/
HTTP/1.1 302 Found
Location: https://www.bilibili.com/video/BV1sa4y1X7Ng/?share_source=copy_web&t=16
X-Powered-By: PHP/8.3
```

服务端直接下发 302，说明分流发生在服务端而不是前端 JS。题面强调"iPhone 独占"，合起来就是典型的 UA cloaking：按 User-Agent 差异化响应。

## 0x01 伪造 iPhone UA

带上 iPhone 的 UA 重新请求：

```
$ curl -A "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1" http://<靶机地址>/
```

这次拿到 200：苹果发布会暗色海报风页面

查看源码

注意：iPad 的 UA 是 `iPad`、Mac 是 `Macintosh`，都不含 `iPhone` 字样，同样被 302——判断词就是字面 `iPhone`。

## 0x02 view-source，注释里的 base64

页面没 flag，看源码。HTML 头部有一段玩梗注释，末尾挂着一串独立的 base64：

```
<!--
  ============================================================
  求你们不要再嘲笑这些题目了
  这个题目是我花了好多token想的 QWQ
  ============================================================
  aGN0Znt0ZXN0X3VhX2NoZWNraW5fMjAyNn0=
-->
```

解码：

```
$ echo "aGN0Znt0ZXN0X3VhX2NoZWNraW5fMjAyNn0=" | base64 -d
hctf{...}
```

拿到 flag。


