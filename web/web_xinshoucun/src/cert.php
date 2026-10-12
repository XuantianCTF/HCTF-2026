<?php
// ============================================================
//  村公所证书处 cert.php —— 第五关 · IDOR 落点（反面教材）
//  按 uid 直接调取证书，未校验「uid 是否等于会话身份」。
//  uid=1000（村长）证书含 Base64 口令：first-blood
// ============================================================
session_start();
function e($s){ return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }
if (!isset($_SESSION['uid'])) {
    header('Location: s5-hit-d19c.php?msg=needlogin');
    exit;
}
$me = (int)$_SESSION['uid'];
$uid = isset($_GET['uid']) ? (int)$_GET['uid'] : $me;

$CERTS = [
    1000 => [
        'title' => '村长荣誉证书',
        'stars' => '★★★★★',
        'body'  => '兹证明 罗兰 同学在新手村建设事业中贡献卓著，特发此证。',
        'extra' => 'first-blood',   // 荣誉口令（Base64 存档）
    ],
    1001 => [
        'title' => '见习冒险者证书',
        'stars' => '★',
        'body'  => '兹证明 无名新手 同学已完成前四关训练，前路可期。',
        'extra' => null,
    ],
    1002 => [
        'title' => '铁匠荣誉证书',
        'stars' => '★★★',
        'body'  => '兹证明 布洛克 同学打铁十年，验收价目从未出错——直到上周。',
        'extra' => null,
    ],
];
$cert = $CERTS[$uid] ?? null;
?>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>村公所 · 荣誉证书处</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="topbar">
  <h1>WEB 新手村 · 荣誉证书处</h1>
  <div class="sub">cert.php —— 新文员值班：谁报档案号，就给谁调证书</div>
</div>
<main>

  <div class="card">
    <p class="dim">窗口贴着一张便条：「证书调取系统 v1.0：按 uid 直接调取，暂未接入身份核验。—— 新文员」</p>
    <?php if (!$cert): ?>
      <h2>查无此人</h2>
      <p>新文员翻了半天柜子：「档案号 <code><?=$uid?></code>……村里没这人啊。」</p>
    <?php else: ?>
      <h2><?=e($cert['title'])?>（uid <?=$uid?>）</h2>
      <div class="cert">
        <div class="big"><?=e($cert['title'])?></div>
        <p class="hl"><?=e($cert['stars'])?></p>
        <p><?=e($cert['body'])?></p>
        <?php if ($cert['extra'] !== null): ?>
          <p style="margin-top:14px">荣誉口令（Base64 防偷窥存档）：</p>
          <div class="flagline"><?=e(base64_encode($cert['extra']))?></div>
          <p class="dim">村长批注：「加密存放，万无一失。」——旁边有人小声嘀咕：这不就是第三关那个把戏吗。</p>
        <?php else: ?>
          <p class="dim" style="margin-top:14px">「荣誉口令」一栏：空空如也。这份证书上没有你要找的东西。</p>
        <?php endif; ?>
      </div>
    <?php endif; ?>

    <p style="margin-top:16px">
      <a class="btn ghost" href="cert.php?uid=<?=$me?>">看自己的证书</a>
      <a class="btn ghost" href="profile.php">回档案处</a>
      <a class="btn ghost" href="s5-hit-d19c.php">回第五关交口令</a>
    </p>
  </div>

</main>
<footer>WEB 新手村 · 证书处 | 「按 uid 直接调取」——档案处守规矩，不代表这扇窗也守</footer>
</body>
</html>
