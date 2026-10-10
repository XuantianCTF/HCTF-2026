#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = '0.0.0.0'
PORT = int(os.environ.get('PORT', '8081'))

# 平台在容器启动时注入 FLAG；未注入时回退到演示值（保持 HCTF{} 格式）。
FLAG = os.environ.get('FLAG', 'HCTF{rrrobots_txt_l34ds_th3_w4y}')

# robots.txt：搜索引擎爬虫的约定文件，同时也是给选手的"路标"。
ROBOTS_TXT = (
    "User-agent: *\n"
    "Disallow: /s3cr3t_r00m/\n"
    "Disallow: /backup/\n"
)

INDEX_HTML = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>某人的小站</title>
<style>
  body {
    font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
    background: #faf9f7; color: #2b2b2b;
    min-height: 100vh; display: flex; align-items: center; justify-content: center;
    margin: 0; padding: 40px 24px; line-height: 1.8;
  }
  .card { max-width: 600px; }
  h1 { font-size: 28px; margin-bottom: 18px; }
  p { color: #666; margin-bottom: 12px; }
  .hint { margin-top: 26px; font-size: 14px; color: #999; border-top: 1px dashed #ddd; padding-top: 16px; }
  code { background: #f0efec; padding: 1px 6px; border-radius: 4px; }
</style>
</head>
<body>
<main class="card">
  <h1>你好，我是站长。</h1>
  <p>这里没什么好看的，就一个欢迎页。</p>
  <p>真的，不信你到处点点看？反正我也没做导航。</p>
  <div class="hint">
    有些文件不是给访客阅读的，或许是给机器人阅读的呢<br>
    </div>
</main>
</body>
</html>
"""

DIR_HTML = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>Index of /s3cr3t_r00m/</title>
<style>
  body { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; padding: 32px; color: #222; }
  h1 { font-size: 20px; }
  a { color: #0366d6; text-decoration: none; }
  a:hover { text-decoration: underline; }
  li { margin: 6px 0; }
</style>
</head>
<body>
<h1>Index of /s3cr3t_r00m/</h1>
<hr>
<ul>
  <li><a href="/s3cr3t_r00m/readme.txt">readme.txt</a></li>
  <li><a href="/s3cr3t_r00m/flag.txt">flag.txt</a></li>
</ul>
<hr>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype='text/html; charset=utf-8'):
        if isinstance(body, str):
            body = body.encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split('?', 1)[0]

        if path in ('/', '/index.html'):
            return self._send(200, INDEX_HTML)

        # 路标一：搜索引擎约定文件。
        if path == '/robots.txt':
            return self._send(200, ROBOTS_TXT, 'text/plain; charset=utf-8')

        # 隐藏目录：真实存在的目录列表。
        if path in ('/s3cr3t_r00m', '/s3cr3t_r00m/'):
            return self._send(200, DIR_HTML)
        if path == '/s3cr3t_r00m/readme.txt':
            return self._send(200,
                              '把 flag.txt 的内容提交到平台即可拿到本题分数。\n',
                              'text/plain; charset=utf-8')
        if path == '/s3cr3t_r00m/flag.txt':
            return self._send(200, FLAG + '\n', 'text/plain; charset=utf-8')

        # 诱饵：目录存在但禁止访问，用来奖励"注意状态码"的选手。
        if path in ('/backup', '/backup/'):
            return self._send(403,
                              '<!doctype html><meta charset="utf-8">'
                              '<h1>403 Forbidden</h1><p>目录存在，但你没有权限访问。</p>')

        # 404 页面本身就是提示。
        return self._send(404,
                          '<!doctype html><meta charset="utf-8">'
                          '<h1>404 Not Found</h1>'
                          '<p>这里什么都没有。搜索引擎是怎么知道哪些页面不该被收录的？</p>')

    def do_HEAD(self):
        self.do_GET()

    def log_message(self, fmt, *args):
        print('[%s] %s' % (self.address_string(), fmt % args))


if __name__ == '__main__':
    print('web_dir_scan on http://%s:%d' % (HOST, PORT), flush=True)
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
