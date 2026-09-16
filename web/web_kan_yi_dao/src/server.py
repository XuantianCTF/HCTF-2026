#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import base64
import json
import os
import random
import secrets
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = '0.0.0.0'
PORT = int(os.environ.get('PORT', '8931'))
ROOT = os.path.dirname(os.path.abspath(__file__))

FLAG_REAL = os.environ.get('FLAG', 'hctf{y0u_4r3_th3_k4ng0d}')  # 平台动态注入，回退值保持 hctf{} 格式
REAL_ORDER = 99999  # 已完成订单：淹没在榜单中游（榜单单号本就 4~6 位混合）

ORDERS = {
    REAL_ORDER: {'owner': 'someone', 'status': 'done', 'goods': 'flag × 1'},
}

LOCK = threading.Lock()
SESSIONS = {}  # sid -> {'order_id': int, 'remaining': float, 'cuts': int}

# ================= curl 蜜罐（渐进门槛 + 永不闭合的碎片流） =================
DECOY_FLAG = 'hctf{w0w_i_know_you_can_do_it}'   # 统一假 flag：TRACK.tok 与蜜罐碎片共用
HP_PATH = '/api/v2/pickup'
HP_HEADER = 'X-Staff-Verify'
HP_CODE_OK = '1'

# 单流节奏与寿命（环境变量可覆盖，便于 exp.py 用短上限验收断开行为）
HP_CAP_SECONDS = float(os.environ.get('KYD_HP_CAP', '3600'))
HP_IVAL_BASE = float(os.environ.get('KYD_HP_IVAL_BASE', '8'))
HP_IVAL_GROW = float(os.environ.get('KYD_HP_IVAL_GROW', '1.9'))
HP_IVAL_MAX = float(os.environ.get('KYD_HP_IVAL_MAX', '110'))
HP_MAX_LINES = 4096        # 单流行数硬上限（双保险）

# 伪造限流与并发护栏
HP_MIN_INTERVAL = 1.5      # 同 IP 两次请求小于该间隔 → 429
HP_RAND_DELAY = (0.4, 2.2)  # 门槛响应前的随机延迟（被限流拖慢的观感）
HP_MAX_STREAMS_IP = 8
HP_MAX_STREAMS_ALL = 64

HP_LOCK = threading.Lock()
HP_IPS = {}                # ip -> {'last': ts, 'streams': n}
HP_STREAMS_ALL = 0

# 三级门槛提示（各用一种编码遮掩，绝不明文下发）
HP_HINT1 = '检测到浏览器会话：本通道仅对命令行工具开放，请使用 curl 重新访问。'
HP_HINT2 = '工具校验通过。员工直领通道需要校验头，头名 X-Staff-Verify。'
HP_HINT3 = '校验头已收到，但校验码不正确。当班校验码：1（整点轮换）。'

# 碎片切分：首段 'hctf{w0w_' 是大钩子；末段（校验位 '}'）永不下发
_HP_NOBRACE = DECOY_FLAG[:-1]                      # 'hctf{w0w_i_know_you_can_do_it'
HP_FRAGS = ['hctf{w0w_', 'i_kn', 'ow_y', 'ou_', 'can', '_do', '_it']  # 7 段 + 永缺的第 8 段


def new_session():
    return {
        'order_id': random.randint(1000, 9999),   # 考生自己的随机订单号
        'remaining': round(random.uniform(0.008, 0.03), 6),
        'cuts': random.randint(35, 58),
    }


class Handler(BaseHTTPRequestHandler):

    # ---------- 基础设施 ----------
    def _send(self, code, obj, set_cookie=None):
        body = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        if set_cookie:
            self.send_header('Set-Cookie', 'sid=%s; Path=/; HttpOnly' % set_cookie)
        self.end_headers()
        self.wfile.write(body)

    def _session(self):
        """取当前会话；无 cookie 或失效则新建并返回 (sess, new_sid)。"""
        sid = None
        for part in self.headers.get('Cookie', '').split(';'):
            k, _, v = part.strip().partition('=')
            if k == 'sid':
                sid = v
                break
        with LOCK:
            sess = SESSIONS.get(sid)
            if sess is None:
                sid = secrets.token_hex(16)
                SESSIONS[sid] = sess = new_session()
                return sess, sid
            return sess, None

    def _body(self):
        try:
            n = int(self.headers.get('Content-Length', 0) or 0)
            return json.loads(self.rfile.read(n) or b'{}')
        except Exception:
            return {}

    # ---------- curl 蜜罐 ----------
    def _hp_text(self, code, payload, charset='utf-8', extra=None):
        """门槛响应：payload 为 str 或原始 bytes，无注入痕迹的纯文本。"""
        body = payload.encode('utf-8') if isinstance(payload, str) else payload
        self.send_response(code)
        self.send_header('Content-Type', 'text/plain; charset=%s' % charset)
        self.send_header('Content-Length', str(len(body)))
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def _hp_gate(self):
        """渐进门槛：返回 True 表示已写完响应（拦下），False 表示放行进流。

        限流时间戳打在"响应发出时"——门槛自带的随机延迟会天然隔开到达时刻，
        打在到达时会让 429 永远打不中快速连发的玩家。"""
        ip = self.client_address[0]
        ua = (self.headers.get('User-Agent') or '').lower()

        with HP_LOCK:
            st = HP_IPS.setdefault(ip, {'last': 0.0, 'streams': 0})
            too_fast = (time.time() - st['last']) < HP_MIN_INTERVAL
        if too_fast:
            time.sleep(0.1)
            with HP_LOCK:
                st['last'] = time.time()
            self._hp_text(429, json.dumps(
                {'ok': False, 'msg': '请求过于频繁，员工通道拥挤，请稍后再试'},
                ensure_ascii=False), extra={'Retry-After': '2'})
            return True
        time.sleep(random.uniform(*HP_RAND_DELAY))
        with HP_LOCK:
            st['last'] = time.time()

        stage = 0
        if 'curl' not in ua:
            stage = 1
            body = base64.b64encode(HP_HINT1.encode('utf-8')).decode('ascii')
            self._hp_text(403, body)
        elif self.headers.get(HP_HEADER) is None:
            stage = 2
            body = base64.b32encode(HP_HINT2.encode('utf-8')).decode('ascii')
            self._hp_text(401, body)
        elif (self.headers.get(HP_HEADER) or '').strip() != HP_CODE_OK:
            stage = 3
            # UTF-8 终端下是乱码；curl ... | iconv -f GBK -t UTF-8 还原
            self._hp_text(403, HP_HINT3.encode('gbk'))
        if stage:
            print('[honeypot] %s stopped at gate G%d' % (ip, stage), flush=True)
            return True
        return False

    def _hp_stream(self):
        """碎片流：管线剧本 → 芝诺间隔分段吐假 flag 碎片 → 末段永在队列 → 超时作废。"""
        global HP_STREAMS_ALL
        ip = self.client_address[0]

        with HP_LOCK:
            st = HP_IPS.setdefault(ip, {'last': 0.0, 'streams': 0})
            if st['streams'] >= HP_MAX_STREAMS_IP or HP_STREAMS_ALL >= HP_MAX_STREAMS_ALL:
                self._hp_text(503, 'channel busy')
                return
            st['streams'] += 1
            HP_STREAMS_ALL += 1

        t0 = time.time()
        lines = 0
        try:
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()

            def w(s):
                self.wfile.write((s + '\n').encode('utf-8'))
                self.wfile.flush()

            w('[网关] 员工直领通道已接入 session=stf_%s' % secrets.token_hex(4))
            w('[风控] 工具指纹校验通过（curl 会话）')
            w('[风控] 员工校验头 X-Staff-Verify 匹配当班码')
            w('[订单] flag × 1 库存已锁定（保留 %d 分钟）' % max(1, int(HP_CAP_SECONDS / 60) - 1))
            w('[核销] 凭据生成完毕，分段下发（共 %d 段，末段为校验位）' % (len(HP_FRAGS) + 1))

            ival = HP_IVAL_BASE
            queue = 3          # 伪造排队人数：缓慢下降后永远卡在 1
            nfrag = len(HP_FRAGS)
            while True:
                if time.time() - t0 >= HP_CAP_SECONDS or lines >= HP_MAX_LINES:
                    break
                time.sleep(min(ival, HP_IVAL_MAX))
                lines += 1
                if lines <= nfrag:
                    pct = min(99.99, 100 * (1 - 0.5 ** (lines / 2.0)))
                    bar = '▓' * max(1, int(pct / 10)) + '░' * (10 - max(1, int(pct / 10)))
                    w('[进度] %.2f%% %s' % (pct, bar))
                    w('[核销] 第 %d/%d 段：%s' % (lines, nfrag + 1, HP_FRAGS[lines - 1]))
                else:
                    if lines % 7 == 0:
                        queue = max(1, queue - 1)
                    w('[进度] 99.99%%（末段占用进度位，等待队列释放）')
                    w('[核销] 校验位仍在生成队列中，前方还有 %d 人' % queue)
                ival = min(ival * HP_IVAL_GROW, HP_IVAL_MAX)

            w('[通道] 会话超时已断开，本次进度已作废，请重新发起')
            print('[honeypot] %s stream ended after %ds (%d stages)' % (ip, time.time() - t0, lines), flush=True)
        except (BrokenPipeError, ConnectionResetError, OSError):
            print('[honeypot] %s stream dropped by client after %ds (%d stages)'
                  % (ip, time.time() - t0, lines), flush=True)
        finally:
            with HP_LOCK:
                st = HP_IPS.get(ip)
                if st:
                    st['streams'] = max(0, st['streams'] - 1)
                HP_STREAMS_ALL = max(0, HP_STREAMS_ALL - 1)

    def log_message(self, fmt, *args):
        print('[%s] %s' % (self.address_string(), fmt % args))

    def do_GET(self):
        if self.path.split('?')[0] == HP_PATH:
            if not self._hp_gate():
                self._hp_stream()
            return

        if self.path == '/' or self.path.startswith('/index'):
            _, sid = self._session()
            try:
                with open(os.path.join(ROOT, 'index.html'), 'rb') as f:
                    html = f.read()
            except OSError:
                return self._send(500, {'ok': False, 'msg': 'index.html missing'})
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(html)))
            if sid:
                self.send_header('Set-Cookie', 'sid=%s; Path=/; HttpOnly' % sid)
            self.end_headers()
            self.wfile.write(html)
            return

        if self.path.startswith('/api/rank'):
            self._session()
            # 运营榜单：35 条，已完成订单淹没在中游——普通手机号名、四位单号、
            # status "已结束"与"已过期清零"同风格、remaining=0.0 与过期单相同（不唯一）
            finished = {
                'rank': 1, 'name': '砍神_阿伟',
                'order_id': REAL_ORDER, 'remaining': 0.0, 'status': '已结束', 'goods': 'flag × 1',
            }
            rows = []
            while len(rows) < 34:
                expired = random.random() < .15
                oid = random.randint(1000, 999999)
                while oid == REAL_ORDER:
                    oid = random.randint(1000, 999999)
                rows.append({
                    'rank': len(rows) + 2,
                    'name': '%d****%04d' % (random.choice([3, 5, 7, 8, 9]), random.randint(0, 9999)),
                    'order_id': oid,
                    'remaining': 0.0 if expired else round(random.uniform(0.004, 0.12), 6),
                    'status': '已过期清零' if expired else '进行中',
                    'goods': 'flag × 1',
                })
            rows.append(finished)
            random.shuffle(rows)  # 数组顺序打乱：消费端按 rank 字段自行排序
            return self._send(200, {'ok': True, 'list': rows})

        return self._send(404, {'ok': False, 'msg': 'not found'})

    def do_POST(self):
        sess, sid = self._session()
        body = self._body()

        if self.path == '/api/kan':
            # cut_total / progress 等字段是客户端上报的表演值，服务端有自己的账本，一概忽略。
            # order_id 信任客户端上报（仅作为"我的砍价单"标签绑定，最后一次为准）。
            try:
                oid = int(str(body.get('order_id')))
                if 1000 <= oid <= 99999:
                    sess['order_id'] = oid
            except (TypeError, ValueError):
                pass
            try:
                strength = float(body.get('strength', 0.3))
                if not (0 < strength < 1):
                    strength = 0.3
            except (TypeError, ValueError):
                strength = 0.3

            with LOCK:
                r = sess['remaining']
                cut = r * strength
                r = round(r - cut, 6)
                if r < 1e-6:
                    r = 1e-6  # 芝诺保底：砍价这条路永远到不了 0（死路）
                sess['remaining'] = r
                sess['cuts'] += 1

            return self._send(200, {
                'ok': True, 'remaining': sess['remaining'],
                'cut': round(cut, 6), 'cut_no': sess['cuts'],
                'msg': '砍价成功，距离拿走 flag 仅剩一步之遥',
            }, set_cookie=sid)

        if self.path == '/api/claim':
            try:
                oid = int(str(body.get('order_id')))
            except (TypeError, ValueError):
                return self._send(200, {'ok': False, 'msg': '当前用户未成功砍下flag'}, set_cookie=sid)
            # [漏洞] 只校验 order_id 是否命中已完成订单，不校验归属人——水平越权冒领
            order = ORDERS.get(oid)
            if order and order['status'] == 'done':
                return self._send(200, {
                    'ok': True, 'msg': '砍价成功，商品（%s）已发出，请查收' % order['goods'],
                    'flag': FLAG_REAL,
                }, set_cookie=sid)
            return self._send(200, {'ok': False, 'msg': '当前用户未成功砍下flag'}, set_cookie=sid)

        if self.path == '/api/share':
            # 表演接口：前端 fire-and-forget，服务端只记账
            return self._send(200, {'ok': True, 'draws': 3, 'msg': '分享成功，奖励已发放'})

        return self._send(404, {'ok': False, 'msg': 'not found'})


if __name__ == '__main__':
    srv = ThreadingHTTPServer((HOST, PORT), Handler)
    print('kan-yi-dao server on http://%s:%d  (Ctrl+C 退出)' % (HOST, PORT))
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
