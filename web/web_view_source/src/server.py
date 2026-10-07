#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = '0.0.0.0'
PORT = int(os.environ.get('PORT', '8080'))
ROOT = os.path.dirname(os.path.abspath(__file__))

# 平台在容器启动时注入 FLAG；未注入时回退到演示值（保持 HCTF{} 格式）。
FLAG = os.environ.get('FLAG', 'HCTF{v13w_s0urc3_1s_4ll_y0u_n33d}')

NOT_FOUND = '<!doctype html><meta charset="utf-8"><h1>404 Not Found</h1><p>页面不存在。</p>'


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
            with open(os.path.join(ROOT, 'index.html'), encoding='utf-8') as f:
                html = f.read().replace('{{FLAG}}', FLAG)
            return self._send(200, html)
        self._send(404, NOT_FOUND)

    def do_HEAD(self):
        self.do_GET()

    def log_message(self, fmt, *args):
        print('[%s] %s' % (self.address_string(), fmt % args))


if __name__ == '__main__':
    print('web_view_source on http://%s:%d' % (HOST, PORT), flush=True)
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
