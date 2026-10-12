<?php
// ============================================================
//  第五关 · 出剑（HIT）—— 考点：登录与会话 / IDOR 越权 /
//  「同站不同接口校验松紧不同」
//  链路：rookie/rookie123 登录 → profile.php（严，只能看自己）
//        → cert.php?uid=1000（松，IDOR）→ Base64 口令 first-blood
//  口令：first-blood
// ============================================================
session_start();
$PASS = 'first-blood';
$USERS = ['rookie' => 'rookie123'];   // 村公所发的见习账号

// 注销
if (isset($_GET['logout'])) {
    session_destroy();
    header('Location: s5-hit-d19c.php');
    exit;
}
// 登录
$loginErr = '';
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST' && isset($_POST['user'])) {
    $u = (string)($_POST['user'] ?? '');
    $p = (string)($_POST['pass'] ?? '');
    if (isset($USERS[$u]) && $USERS[$u] === $p) {
        $_SESSION['uid'] = 1001;   // 见习冒险者档案号
        header('Location: profile.php');
        exit;
    }
    $loginErr = '村公所窗口：「账号或口令不对。」（账号密码就在任务卡上，别紧张。）';
}
// 通关口令
$passed = false; $err = '';
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST' && isset($_POST['pw'])) {
    $got = strtolower(trim((string)($_POST['pw'] ?? '')));
    if ($got === $PASS) { $passed = true; }
    else { $err = '罗兰摇头：「口令在我的荣誉证书上——用你的眼睛去看不该看的档案编号。」'; }
}
function e($s){ return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }
$logged = isset($_SESSION['uid']);
?>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>第五关 · 出剑 HIT</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="topbar">
  <h1>WEB 新手村 · 第五关</h1>
  <div class="sub">出剑 HIT —— 前四件装备合体，打出真正的第一击</div>
  <div class="dots"><span class="on">●</span><span class="on">●</span><span class="on">●</span><span class="on">●</span><span class="now">●</span><span class="off">○</span></div>
</div>
<main>

  <div class="card">
    <div class="npc">
      <div class="avatar">剑</div>
      <div>
        <div class="who">村长 · 罗兰（退役冒险者队长）</div>
        <div class="bubble">
          <p>眼、声、手、图，四件装备都在身上了。最后这一课，我教<b>越权</b>——出村后的第一击，也是真实世界里最常见的一击。</p>
          <p>旧地图室那份备份是我留的，脸红。将功补过，最后一关我亲自坐镇村公所。</p>
        </div>
      </div>
    </div>
  </div>

  <div class="card">
    <h2>第五课 · 手环、编号与「谁可以看谁」</h2>

    <h3>1. 登录 = 领手环（Cookie / Session）</h3>
    <p>你在登录框输入账号密码，服务器验明正身后发给你一只<b>手环</b>（一串 Cookie，比如 <code>PHPSESSID=xxx</code>）。
    之后你的每个请求都自动戴着手环，服务器凭手环认人——<b>「你是谁」这件事，从此记在服务器心里，不靠页面说了算</b>。</p>

    <h3>2. IDOR：只查编号、不问来人的接口</h3>
    <p>很多接口长这样：<code>profile.php?uid=1001</code>——「报档案号，给你看档案」。
    编号（uid）是<b>你随手可改的输入</b>。如果服务器只顾着按编号查数据，<b>忘了检查这个编号是不是你本人</b>，
    把 uid 一改，你就戴着自己的手环、看了<b>别人的柜子</b>。这就是越权（IDOR，不安全的直接对象引用），真实世界里海量数据泄露都源于它。</p>

    <h3>3. 同一个网站，柜员松紧不一</h3>
    <p>关键心得：<b>档案处管得严的村公所，证书处未必</b>。一个接口安全不代表接口背后的兄弟接口都安全——
    探险家教会你「找地方」，这一课教你「每个门口都敲一敲」。</p>
    <p class="dim">预防针：本关 <code>profile.php</code> 是<b>正面教材</b>（改 uid 会真的被拒）——被拒的地方别死磕，换隔壁柜台。</p>
  </div>

<?php if ($passed): ?>
  <div class="card reward">
    <h2>通关！罗兰起身，把佩剑郑重递给你</h2>
    <div class="equip">
      <div class="glyph">剑</div>
      <div class="name">出村之剑 · SWORD</div>
      <div class="code">SWORD</div>
    </div>
    <p>「first-blood——<b>第一滴血</b>。这是冒险者生涯的第一次真正的『打』：你戴着自己的手环，看了别人的证书。记住这把剑的重量，也记住：<b>用它保护，而不是作恶</b>。」</p>
    <div class="flagline">碎片 5 / 5 ：SWORD</div>
    <p>五件装备集齐。出村的毕业门就在眼前——去吧。</p>
    <p style="margin-top:16px"><a class="btn green" href="graduate-a67f.php">走向毕业门</a></p>
  </div>
<?php else: ?>
  <div class="card quest">
    <h2>任务 · 村长的荣誉证书</h2>
    <p class="goal">本关口令写在<b>村长（罗兰）的荣誉证书</b>上（Base64 存档，村长管这叫防偷窥——你已经在第三关见过这种把戏）。你的任务：以见习冒险者身份，看到它。</p>
    <ul>
      <li>村公所已为你注册见习账号：<code>rookie</code> / <code>rookie123</code>（下发账号，拿去登录即可）。</li>
      <li>登录后进入<b>档案处</b>（profile.php）。档案处管得严：<b>只能看自己的档案</b>。</li>
      <li>但村志上记着所有村民的档案号（uid）——包括村长的。而<b>荣誉证书处（cert.php）是新文员值班</b>……</li>
      <li>你的手环是真的，编号是随便填的。第四课第二段，再读一遍。</li>
    </ul>

    <?php if (!$logged): ?>
    <h3>村公所登录窗口</h3>
    <form method="post" class="gate">
      <input type="text" name="user" placeholder="账号（见任务卡）" autocomplete="off">
      <input type="password" name="pass" placeholder="口令">
      <button class="btn" type="submit">登录村公所</button>
    </form>
    <?php if ($loginErr): ?><div class="err-box"><?=e($loginErr)?></div><?php endif; ?>
    <?php if (isset($_GET['msg']) && $_GET['msg'] === 'needlogin'): ?>
      <div class="err-box">档案处：「先在下面窗口领手环（登录），没手环的谢绝入内。」</div>
    <?php endif; ?>
    <?php else: ?>
    <p class="ok-text">你已佩戴村公所手环（UID <?=e($_SESSION['uid'])?>）。</p>
    <p>
      <a class="btn ghost" href="profile.php">前往档案处</a>
      <a class="btn ghost" href="s5-hit-d19c.php?logout=1">注销（换个新手重来）</a>
    </p>
    <?php endif; ?>

    <?php if ($logged): ?>
    <hr style="border:none;border-top:1px dashed var(--line);margin:16px 0">
    <form method="post" class="gate">
      <input type="text" name="pw" placeholder="输入村长证书上的口令" autocomplete="off">
      <button class="btn" type="submit">向罗兰提交</button>
    </form>
    <?php if ($err): ?><div class="err-box"><?=e($err)?></div><?php endif; ?>
    <?php endif; ?>
  </div>

  <div class="card">
    <h2>卡住了？看提示</h2>
    <details class="hint">
      <summary>提示一：方向</summary>
      <div class="hint-body">登录后先进档案处，看清村志上<b>村长的档案号</b>。档案处改 uid 会被拒（它是正面教材）——但档案处页面里有「查看我的荣誉证书」的链接，注意看那个链接<b>长什么样</b>（cert.php?uid=...）。换个档案号再访问证书处试试。</div>
    </details>
    <details class="hint">
      <summary>提示二：具体操作</summary>
      <div class="hint-body">
        <p>登录后，浏览器地址栏直接访问：</p>
        <pre>http://&lt;服务地址&gt;/cert.php?uid=1000</pre>
        <p>（1000 是村长的档案号——地址栏本身就是你改参数最快的地方。）证书上的口令是 Base64 存档，F12 → Console 用 <code>atob("那串")</code> 解开。</p>
      </div>
    </details>
  </div>
<?php endif; ?>

</main>
<footer>WEB 新手村 · 第五关 出剑 | 拿到手环只说明你是你，不说明你能看所有人</footer>
</body>
</html>
