<?php
// ============================================================
// web_growcode —— 会生长的源码
// 引擎：无状态层级触发 + 累计过滤 + 降权执行
// 约定：各层"展示源码"与真实过滤逻辑共用同一份常量与文案，
//       保证选手审计到的就是真实生效的规则
// ============================================================

$REAL_FLAG = getenv('FLAG') ?: 'hctf{GR0W1NG_S0URC3_L1N3_BY_L1N3}';
putenv('FLAG'); // 即刻从进程环境清除 FLAG（配合部署侧 su 降权，封死 /proc 泄露）

$BLACKLIST = '/flag|cat|tac|nl|head|tail|more|less|sort|strings|rev|base64|xxd|hexdump|grep|sed|awk|env|printenv|export|proc|passwd|shadow|secret|uname|curl|wget|nc|php/i';
$MAXLEN = 16;
$MSG_BLOCK = '检测到敏感关键字，请求已被拦截（分隔符与特殊字符同样在监控范围内）';

// ---- 各层展示源码文本（与真实过滤一一对应）----
// 展示文件恒以唯一的 system($cmd); 收尾，各层判断依次插在它之前
$SRC_L1 = <<<'PHPT'
<?php
// index.php —— 在线命令小助手
// 用法：在地址栏输入 ?cmd=命令

$cmd = $_GET['cmd'] ?? '';
PHPT;

$SRC_L2 = <<<'PHPT'

$blacklist = '{BLACKLIST}';

if (preg_match($blacklist, $cmd)) {
    exit('{MSGBLOCK}');
}
PHPT;

$SRC_L3 = <<<'PHPT'

$cmd = preg_replace('/\s+/', '', $cmd);

if (strlen($cmd) > {MAXLEN}) {
    exit('命令长度超出限制（最多 {MAXLEN} 字符）');
}
PHPT;

$SRC_L4 = <<<'PHPT'

$auth = false;

// 从 POST 数据中还原参数（注意：会覆盖同名变量）
extract($_POST);

if (preg_match($blacklist, $cmd) || strlen($cmd) > {MAXLEN}) {
    exit('检测到敏感关键字或长度超限，请求已被拦截');
}

if ($cmd === 's' && $auth === 'admin') {
    exit($REAL_FLAG);
}
PHPT;

// ---- 层级配置：展示源码 + 触发判定（只看当前请求，无状态）----
$LEVELS = [
    2 => [
        'src'     => str_replace(['{BLACKLIST}', '{MSGBLOCK}'], [$BLACKLIST, $MSG_BLOCK], $SRC_L2),
        'trigger' => fn(string $cmd): bool => preg_match($BLACKLIST, $cmd) === 1,
    ],
    3 => [
        'src'     => str_replace('{MAXLEN}', (string)$MAXLEN, $SRC_L3),
        'trigger' => fn(string $cmd): bool => preg_match('/[|;&><]/', $cmd) === 1,
    ],
    4 => [
        'src'     => str_replace('{MAXLEN}', (string)$MAXLEN, $SRC_L4),
        'trigger' => fn(string $cmd, array $post): bool => $post !== [] || preg_match('/[`${]/', $cmd) === 1,
    ],
];

// ---- 主流程：计算当前请求达到的最高层级 ----
$cmd = $_GET['cmd'] ?? '';
$level = 1;
foreach ($LEVELS as $n => $lv) {
    if ($lv['trigger']($cmd, $_POST)) {
        $level = $n;
    }
}

// ---- 按累计层级应用过滤并执行（与展示源码逐行对应）----
$out = '';
$blocked = '';
$strippedNote = '';

if ($level >= 2 && preg_match($BLACKLIST, $cmd)) {
    $blocked = $MSG_BLOCK;
}
if ($blocked === '' && $level >= 3) {
    $stripped = preg_replace('/\s+/', '', $cmd);
    if ($stripped !== $cmd) {
        $strippedNote = '[去空白后] ' . $stripped;
    }
    $cmd = $stripped;
    if (strlen($cmd) > $MAXLEN) {
        $blocked = '命令长度超出限制（最多 ' . $MAXLEN . ' 字符）';
    }
}
if ($blocked === '' && $level >= 4) {
    $auth = false;
    extract($_POST);
    if (preg_match($BLACKLIST, $cmd) || strlen($cmd) > $MAXLEN) {
        $blocked = '检测到敏感关键字或长度超限，请求已被拦截';
    } elseif ($cmd === 's' && $auth === 'admin') {
        $out = $REAL_FLAG;
    }
}
if ($blocked === '' && $out === '' && $cmd !== '') {
    $out = run_cmd($cmd);
}

// 部署层沙箱：选手命令一律限时并降权到 www-data 执行，
// 使其对 root 进程的 /proc 不可读（见 writeup 的安全设计说明）
function run_cmd(string $c): string
{
    $safe = escapeshellarg($c);
    return (string)shell_exec("timeout 3 su -s /bin/sh www-data -c {$safe} 2>&1");
}

// ---- 渲染：按 1..level 拼接展示源码，system 恒在末尾，行号连续，无缝衔接 ----
$visible = $SRC_L1;
foreach ($LEVELS as $n => $lv) {
    if ($n <= $level) {
        $visible .= "\n" . $lv['src'];
    }
}
$visible .= "\n\nsystem(\$cmd);";
$visible = rtrim($visible, "\r\n") . "\n";

$codeHtml = highlight_string($visible, true);
$lineTotal = substr_count($visible, "\n");
$lnHtml = implode("\n", range(1, $lineTotal));

$echo = '';
if ($cmd !== '' || $blocked !== '' || $out !== '' || $strippedNote !== '') {
    $echo = ($_GET['cmd'] ?? '') !== '' ? '> ' . $_GET['cmd'] . "\n" : '';
    if ($strippedNote !== '') {
        $echo .= $strippedNote . "\n";
    }
    if ($blocked !== '') {
        $echo .= $blocked;
    } elseif ($out !== '') {
        $echo .= $out;
    }
}
$echoHtml = htmlspecialchars($echo, ENT_QUOTES, 'UTF-8');
?>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>index.php</title>
<style>
body { background: #ffffff; margin: 8px; }
.wrap { display: flex; overflow-x: auto;
        font: 13px/1.5 Consolas, Menlo, "DejaVu Sans Mono", monospace; }
pre { margin: 0; padding: 0; }
.ln { color: #c9c9c9; text-align: right; flex: 0 0 auto; white-space: pre;
      margin-right: 1em; user-select: none; -webkit-user-select: none; }
.code { white-space: pre; }
.out { margin: 0.75em 0 0; white-space: pre-wrap; word-break: break-all;
       font: 13px/1.5 Consolas, Menlo, "DejaVu Sans Mono", monospace; }
</style>
</head>
<body>
<div class="wrap"><pre class="ln"><?=$lnHtml?></pre><pre class="code"><?=$codeHtml?></pre></div>
<?php if ($echo !== ''): ?><pre class="out"><?=$echoHtml?></pre><?php endif; ?>
</body>
</html>
