#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kan-yi-dao 前端构建脚本（出题方工具，勿外发，产物进容器）。

从 src/index.dev.html（可读母版）构建 src/index.html 与 src/page.html：
  1. JS 去注释（字符串感知；出题指路注释一并消失）
  2. IIFE 包裹，内联 onclick 引用的全局函数（closeMask/retainYes/retainNo）挂回 window
  3. javascript-obfuscator 全量混淆（node>=18，writeup/tools 下 npm install）：
     全标识符十六进制重命名 + 字符串数组 base64 化（端点串等全部消失于明文）
     - reservedStrings 豁免 16+ 位 base64 形态字面量：TRACK.tok 留在原位，
       exp.py 的 `tok: '...'` 正则与 _tk() 运行时解码不受影响
     - 不开控制流扁平化/死代码注入/debugProtection（保性能、非敌意）
  4. 混淆产物之前注入 var __bp = "<零宽位流>";（字面 U+200B/U+200C，
     字符串数组化会毁灭字面零宽，故必须绕过混淆器）
构建后自检：零宽回读、tok 字面量在位且解码正确、端点串/99999/旧标识符不残留、
onclick 导出齐全、混淆确实发生（_0x 存在）。

用法：python writeup/tools/build_frontend.py  （在题目根目录执行）
"""
import base64
import io
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, '..', '..', 'src'))

ZW_TEXT = '偷偷告诉你个口子：/api/v2/pickup，条件让它自己说（我没提醒你（bushi'
DECOY_FLAG = 'hctf{w0w_i_know_you_can_do_it}'
TOK = base64.b64encode(bytes(b ^ 90 for b in DECOY_FLAG.encode())).decode()

JUICY_IDENTIFIERS = ['TRACK', '_tk', 'fetchRank', 'renderRank', 'apiRow', 'genOthers',
                     'RANKrows', 'OTHERS', 'showClaimOK', 'LS_KEY']
ENDPOINTS = ['/api/rank', '/api/kan', '/api/share', '/api/claim']
EXPORTS = {'closeMask', 'retainYes', 'retainNo'}


def strip_js_comments(js):
    out = []
    i, n = 0, len(js)
    state = 'code'  # code | sq | dq | tpl | lc | bc
    while i < n:
        c = js[i]
        nxt = js[i + 1] if i + 1 < n else ''
        if state == 'code':
            if c == "'":
                state = 'sq'; out.append(c); i += 1
            elif c == '"':
                state = 'dq'; out.append(c); i += 1
            elif c == '`':
                state = 'tpl'; out.append(c); i += 1
            elif c == '/' and nxt == '/':
                state = 'lc'; i += 2
            elif c == '/' and nxt == '*':
                state = 'bc'; i += 2
            else:
                out.append(c); i += 1
        elif state in ('sq', 'dq', 'tpl'):
            if c == '\\':
                out.append(c)
                if nxt:
                    out.append(nxt)
                i += 2
            elif (state == 'sq' and c == "'") or (state == 'dq' and c == '"') or (state == 'tpl' and c == '`'):
                state = 'code'; out.append(c); i += 1
            else:
                out.append(c); i += 1
        elif state == 'lc':
            if c == '\n':
                state = 'code'; out.append(c); i += 1
            else:
                i += 1
        else:  # bc
            if c == '*' and nxt == '/':
                state = 'code'; i += 2
            else:
                i += 1
    return ''.join(out)


def zw_encode(text):
    bits = ''.join(format(b, '08b') for b in text.encode('utf-8'))
    return ''.join('\u200b' if b == '0' else '\u200c' for b in bits)


def zw_decode(s):
    bits = ''.join('0' if ch == '\u200b' else '1' for ch in s if ch in '\u200b\u200c')
    raw = bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits) // 8 * 8, 8))
    return raw.decode('utf-8', 'replace')


def obfuscate(js):
    """调用 node + javascript-obfuscator（依赖装在 writeup/tools）。"""
    runner = os.path.join(HERE, 'obfuscate_runner.js')
    node_modules = os.path.join(HERE, 'node_modules')
    if not os.path.isdir(node_modules):
        sys.exit('FATAL: writeup/tools/node_modules missing - run "npm install" there first')
    fin = os.path.join(HERE, '_obf_in.tmp.js')
    fout = os.path.join(HERE, '_obf_out.tmp.js')
    io.open(fin, 'w', encoding='utf-8', newline='\n').write(js)
    try:
        subprocess.run(['node', runner, fin, fout], check=True, cwd=HERE)
        return io.open(fout, encoding='utf-8').read()
    finally:
        for p in (fin, fout):
            if os.path.exists(p):
                os.remove(p)


def build():
    dev = io.open(os.path.join(SRC, 'index.dev.html'), encoding='utf-8').read()
    m = re.search(r'<script>\n(.*)\n</script>', dev, re.S)
    if not m:
        sys.exit('FATAL: <script> block not found in index.dev.html')
    js = m.group(1)
    js = strip_js_comments(js)

    exports = 'window.closeMask=closeMask;window.retainYes=retainYes;window.retainNo=retainNo;'
    wrapped = "(function(){\n%s\n%s\n})();" % (js, exports)
    obf = obfuscate(wrapped)

    # 零宽载体必须绕过混淆器（字符串数组化会毁灭字面 U+200B/U+200C），以独立语句前置注入
    zw = zw_encode(ZW_TEXT)
    js_out = 'var __bp = "%s";\n%s' % (zw, obf)

    html = dev[:m.start()] + '<script>\n' + js_out + '\n</script>' + dev[m.end():]
    for out_name in ('index.html', 'page.html'):
        io.open(os.path.join(SRC, out_name), 'w', encoding='utf-8', newline='\n').write(html)
    return html, js_out


def selfcheck(html, js_out):
    errs = []

    def chk(name, ok, detail=''):
        print('%s %s%s' % ('[PASS]' if ok else '[FAIL]', name, (' - ' + detail) if detail else ''))
        if not ok:
            errs.append(name)

    chk('zw roundtrip == expected lure text', zw_decode(html) == ZW_TEXT, zw_decode(html)[:50])
    # 混淆器会把对象键引号化：tok:'...' 变 'tok':'...'；数字 90 变 0x5a
    tok = re.search(r"[\"']?tok[\"']?\s*:\s*'([^']+)'", html)
    decoy = ''.join(chr(b ^ 90) for b in base64.b64decode(tok.group(1))) if tok else ''
    chk('tok literal kept in place by reservedStrings', bool(tok))
    chk('tok decodes to uniform decoy flag', decoy == DECOY_FLAG, decoy)
    chk('tok value matches generator', tok and tok.group(1) == TOK)
    chk('no plaintext endpoints in script', not any(ep in js_out for ep in ENDPOINTS))
    chk('no 99999 / real-flag / IDOR leak',
        not re.search(r'(?<!\d)99999(?!\d)', html) and not any(s in html for s in ('IDOR', 'hctf{')),
        '99999 only allowed as substring of larger numbers (share-link rndInt range)')
    chk('old juicy identifiers gone (obfuscated)',
        not any(re.search(r'\b%s\b' % k, js_out) for k in JUICY_IDENTIFIERS))
    chk('hex rename actually happened', re.search(r'\b_0x[0-9a-f]{4,}\b', js_out) is not None)
    # 混淆后导出行是 window[_0x..]=.. 运行时计算属性，无法静态 grep——
    # 静态只校验母版的内联 onclick 清单齐全，运行时正确性交给浏览器冒烟
    dev = io.open(os.path.join(SRC, 'index.dev.html'), encoding='utf-8').read()
    inline = set(re.findall(r'on\w+\s*=\s*"([A-Za-z_$][\w$]*)\s*\(', dev))
    chk('all inline onclick globals exported (master)',
        inline <= EXPORTS, 'found: %s' % sorted(inline))
    chk('window export calls present in obfuscated tail',
        len(re.findall(r'window\[', js_out)) >= len(EXPORTS))
    return errs


if __name__ == '__main__':
    html, js_out = build()
    print('built index.html/page.html: %d bytes (script %d bytes)'
          % (len(html.encode('utf-8')), len(js_out.encode('utf-8'))))
    errs = selfcheck(html, js_out)
    sys.exit(1 if errs else 0)
