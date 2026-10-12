<?php
// ============================================================
//  驿站内部柜台 messenger.php —— 第二关实操接口
//  校验：User-Agent === RookieCourier/1.0 且
//        Referer === https://elders.village.gov/
//  三态渐进式报错：每一层报错本身都是教学引导。
// ============================================================
function e($s){ return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }
$ua  = $_SERVER['HTTP_USER_AGENT'] ?? '';
$ref = $_SERVER['HTTP_REFERER'] ?? '';
?>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>驿站内部柜台</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="topbar">
  <h1>WEB 新手村 · 驿站内部柜台</h1>
  <div class="sub">messenger.php —— 只接待真正的信使</div>
</div>
<main>

<?php if ($ua !== 'RookieCourier/1.0'): ?>
  <div class="card">
    <h2>闭门羹 · 第一道</h2>
    <div class="npc">
      <div class="avatar">柜</div>
      <div>
        <div class="who">柜台窗口</div>
        <div class="bubble">
          <p>「口令？口令只给<b>信使</b>看。你这张名片不像信使。」</p>
        </div>
      </div>
    </div>
    <p>柜台瞄了一眼你的名片（User-Agent），记下了这个：</p>
    <pre>User-Agent: <?=e($ua ?: '(空)')?></pre>
    <p>要自称见习信使 <code>RookieCourier/1.0</code>——浏览器替你写的名片做不了主，
    用第二课学的方式<b>自己寄信</b>、自己署名。</p>
    <p class="dim">（这里没有表单给你填：柜台看的是请求头，不是页面输入框。）</p>
  </div>

<?php elseif ($ref !== 'https://elders.village.gov/'): ?>
  <div class="card">
    <h2>闭门羹 · 第二道</h2>
    <div class="npc">
      <div class="avatar">柜</div>
      <div>
        <div class="who">柜台窗口</div>
        <div class="bubble">
          <p>「名片对了，是个信使。不过——<b>介绍信呢？</b>」</p>
        </div>
      </div>
    </div>
    <p>柜台翻了翻你这次的请求，你的来路（Referer）是：</p>
    <pre>Referer: <?=e($ref ?: '(空——直接请求，没有来路)')?></pre>
    <p>驿站只认<b>长老会</b>抬头的介绍信，抬头必须一字不差：</p>
    <pre>Referer: https://elders.village.gov/</pre>
    <p class="ok-text">进展不错——身份已验过，只差信头最后一项。同一封信里补上它。</p>
  </div>

<?php else: ?>
  <div class="card reward">
    <h2>回执 · 身份核验通过</h2>
    <p>柜台收下信，盖章，递出一张回执：</p>
    <div class="flagline">口令：say-hello</div>
    <p>「这是你这次请求在服务器眼里的<b>完整模样</b>——留个纪念，你已经是能亲手写信的人了。」</p>
<pre>GET /messenger.php HTTP/1.1
Host: <?=e($_SERVER['HTTP_HOST'] ?? 'village.example.com')?>
User-Agent: RookieCourier/1.0
Referer: https://elders.village.gov/

（这封信用了两张「名片」，全是你亲手署的名。）</pre>
    <p style="margin-top:14px"><a class="btn green" href="s2-speak-7c21.php">拿口令回第二关，向梅琳提交</a></p>
  </div>
<?php endif; ?>

</main>
<footer>WEB 新手村 · 驿站内部柜台 | 报错是服务器在跟你说话，逐字读完</footer>
</body>
</html>
