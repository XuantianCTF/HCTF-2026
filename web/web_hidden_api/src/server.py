#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

HOST = '0.0.0.0'
PORT = int(os.environ.get('PORT', '8082'))
ROOT = os.path.dirname(os.path.abspath(__file__))

# 平台在容器启动时注入 FLAG；未注入时回退到演示值（保持 HCTF{} 格式）。
FLAG = os.environ.get('FLAG', 'HCTF{j4v4scr1pt_1s_publ1c}')

# 前端 app.js 里 base64 硬编码的调试 key（atob("bGV0bWVpbl8yMDI2") == letmein_2026）。
DEBUG_KEY = 'letmein_2026'


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype='text/html; charset=utf-8'):
        if isinstance(body, str):
            body = body.encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _file(self, name):
        with open(os.path.join(ROOT, name), 'rb') as f:
            return f.read()

    def do_GET(self):
        url = urlparse(self.path)
        path = url.path

        if path in ('/', '/index.html'):
            return self._send(200, self._file('index.html'))
        if path == '/static/app.js':
            return self._send(200, self._file('app.js'),
                              'application/javascript; charset=utf-8')

        # 隐藏接口：key 正确才返回 flag。
        if path == '/api/v2/backup':
            key = parse_qs(url.query).get('key', [''])[0]
            if key == DEBUG_KEY:
                return self._send(200, json.dumps(
                    {'ok': True, 'flag': FLAG}, ensure_ascii=False),
                    'application/json; charset=utf-8')
            return self._send(403, json.dumps(
                {'ok': False, 'msg': 'forbidden'}), 'application/json; charset=utf-8')

        return self._send(404,
                          '<!doctype html><meta charset="utf-8">'
                          '<h1>404 Not Found</h1>')

    def do_POST(self):
        path = urlparse(self.path).path
        if path == '/api/v2/login':
            # 前端登录永远失败，让选手把注意力放到审计前端代码上。
            return self._send(200, json.dumps(
                {'ok': False, 'msg': '用户名或密码错误'},
                ensure_ascii=False), 'application/json; charset=utf-8')
        return self._send(404, json.dumps({'ok': False, 'msg': 'not found'}),
                          'application/json; charset=utf-8')

    def do_HEAD(self):
        self.do_GET()

    def log_message(self, fmt, *args):
        print('[%s] %s' % (self.address_string(), fmt % args))


if __name__ == '__main__':
    print('web_hidden_api on http://%s:%d' % (HOST, PORT), flush=True)
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
