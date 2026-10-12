<?php
// ============================================================
//  村公所档案处 profile.php —— 第五关 · 正面教材（校验严格）
//  服务端校验 uid 必须等于会话身份：直接改 uid 看别人会被拒。
//  （与 cert.php 形成对照：同站不同接口，校验松紧不同）
// ============================================================
session_start();
function e($s){ return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }
if (!isset($_SESSION['uid'])) {
    header('Location: s5-hit-d19c.php?msg=needlogin');
    exit;
}
$me = (int)$_SESSION['uid'];   // 见习冒险者固定 1001

$VILLAGE = [
    1000 => ['name' => '罗兰',      'title' => '村长 · 退役冒险者队长', 'coins' => '???'],
    1001 => ['name' => '无名新手',  'title' => '见习冒险者（你）',      'coins' => '10'],
    1002 => ['name' => '布洛克',    'title' => '铁匠',                  'coins' => '???'],
];

$askUid = isset($_GET['uid']) ? (int)$_GET['uid'] : $me;
$isOther = ($askUid !== $me);
?>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>村公所 · 档案处</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="topbar">
  <h1>WEB 新手村 · 村公所档案处</h1>
  <div class="sub">profile.php —— 老档案员值班，管得很严</div>
</div>
<main>

<?php if ($isOther): ?>
  <div class="card">
    <h2>档案处 · 拒绝查阅</h2>
    <p>老档案员扶了扶眼镜，把你要查的档案合上了：</p>
    <p class="err-text">「档案号 <?=$askUid?> 不是你本人（你的会话身份是 <?=$me?>）。
    《村公所档案条例》第一条：<b>只能查阅本人档案</b>。这儿不兴看别人的。」</p>
    <p class="dim">（这一关它是<b>正面教材</b>：服务端校验了「uid 必须等于会话身份」，改编号在这儿行不通。被拒是正常的——死磕一个上锁的柜子不如去敲敲隔壁的门。档案处的页面上，就有通往隔壁的链接。）</p>
    <p>
      <a class="btn ghost" href="profile.php">回到我的档案</a>
      <a class="btn ghost" href="s5-hit-d19c.php?logout=1">注销</a>
    </p>
  </div>

<?php else: ?>
  <div class="card">
    <h2>我的档案</h2>
    <table class="grid">
      <tr><th>档案号 uid</th><th>姓名</th><th>身份</th><th>金币</th></tr>
      <tr><td class="hl"><?=$me?></td><td><?=$VILLAGE[$me]['name']?></td><td><?=$VILLAGE[$me]['title']?></td><td><?=$VILLAGE[$me]['coins']?></td></tr>
    </table>
    <p>老档案员递还你的档案：「保管好手环。<b>荣誉证书在隔壁窗口</b>，按档案号直接调取——那是新文员在管，跟我这儿规矩不一样。」</p>
    <p>
      <a class="btn" href="cert.php?uid=<?=$me?>">查看我的荣誉证书（cert.php?uid=<?=$me?>）</a>
    </p>
    <p class="dim">——留意一下这个链接的地址长什么样。</p>
  </div>

  <div class="card">
    <h2>村志 · 在册村民</h2>
    <table class="grid">
      <tr><th>档案号 uid</th><th>姓名</th><th>身份</th></tr>
      <?php foreach ($VILLAGE as $uid => $v): ?>
      <tr><td class="hl"><?=$uid?></td><td><?=e($v['name'])?></td><td><?=e($v['title'])?></td></tr>
      <?php endforeach; ?>
    </table>
    <p class="dim">村长的档案号是 <b>1000</b>。想看他的档案？档案处不让。但「证书处」是另一回事——</p>
    <p>
      <a class="btn ghost" href="cert.php?uid=<?=$me?>">去证书处（先看看自己的）</a>
      <a class="btn ghost" href="s5-hit-d19c.php?logout=1">注销</a>
    </p>
  </div>
<?php endif; ?>

</main>
<footer>WEB 新手村 · 档案处 | 这扇门守规矩——不代表整栋楼都守规矩</footer>
</body>
</html>
