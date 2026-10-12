<?php
// ============================================================
//  铁匠铺柜台 forge.php —— 第三关实操接口
//  校验：POST / item=sword-blueprint / 1 <= price <= 10（钱包余额）
//  成功返回 Base64 密文（ASCII 明文，atob 可直接解）
//  口令：smith-hand
// ============================================================
function e($s){ return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }
$WALLET = 10;
$item = (string)($_POST['item'] ?? '');
$priceRaw = $_POST['price'] ?? null;
$price = is_numeric($priceRaw) ? (int)$priceRaw : null;
?>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>铁匠铺柜台</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="topbar">
  <h1>WEB 新手村 · 铁匠铺柜台</h1>
  <div class="sub">forge.php —— 柜台只认订单上写的价格</div>
</div>
<main>

<?php if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST'): ?>
  <div class="card">
    <h2>柜台打烊姿势不对</h2>
    <p>铁匠头也不抬：「单子要从铺子的<b>订单按钮</b>递进来（POST 到本柜台）。空着手 GET 我一眼，是没有图纸的。」</p>
    <p><a class="btn ghost" href="s3-forge-b55d.php">回铁匠铺</a></p>
  </div>

<?php elseif ($item !== 'sword-blueprint'): ?>
  <div class="card">
    <h2>订单有误</h2>
    <p>铁匠看了半天：「这单我没接过（item 不对）。铺子里卖的只有一样：<code>sword-blueprint</code>。」</p>
    <p><a class="btn ghost" href="s3-forge-b55d.php">回铁匠铺重新下单</a></p>
  </div>

<?php elseif ($price === null): ?>
  <div class="card">
    <h2>订单没有价格</h2>
    <p>铁匠：「价格（price）都没写，我收你什么？」</p>
    <p><a class="btn ghost" href="s3-forge-b55d.php">回铁匠铺重新下单</a></p>
  </div>

<?php elseif ($price > $WALLET): ?>
  <div class="card">
    <h2>柜台 · 账本不答应</h2>
    <div class="npc">
      <div class="avatar">匠</div>
      <div>
        <div class="who">铁匠 · 布洛克</div>
        <div class="bubble">
          <p>「验钞机没拦住你，我的<b>账本</b>拦住了：订单 <?=$price?> 金币，钱包只有 <?=$WALLET?>。」</p>
          <p>「不过嘛……」他敲了敲订单，「订单上的价格，<b>是客人自己填的</b>。你说是吧？」</p>
        </div>
      </div>
    </div>
    <p class="dim">服务端校验了「价格不得超过钱包余额」，但它信任的是订单字段本身——橱窗标价牌只是标价牌。</p>
    <p><a class="btn ghost" href="s3-forge-b55d.php">回铁匠铺</a></p>
  </div>

<?php elseif ($price < 1): ?>
  <div class="card">
    <h2>柜台 · 铁匠的底线</h2>
    <p>铁匠把锤子往砧子上一放，火星四溅：</p>
    <p>「<b><?=$price?> 金币？</b>不赊账、不白送。价格必须 <b>≥ 1</b> 且 <b>≤ <?=$WALLET?></b>——想白嫖图纸，门儿都没有。」</p>
    <p class="dim">（服务端校验下界：这题不考负数/零元购，考的是「改成一个付得起的价格」。）</p>
    <p><a class="btn ghost" href="s3-forge-b55d.php">回铁匠铺重新下单</a></p>
  </div>

<?php else: ?>
  <?php
  // 成交：图纸密文（ASCII 明文，玩家用 atob / CyberChef 解码得口令）
  $plaintext = "Blueprint delivered! Blacksmith Broc engraved on the corner: the passcode is smith-hand";
  $cipher = base64_encode($plaintext);
  ?>
  <div class="card reward">
    <h2>成交 · 图纸已交付（密文版）</h2>
    <div class="npc">
      <div class="avatar">匠</div>
      <div>
        <div class="who">铁匠 · 布洛克</div>
        <div class="bubble">
          <p>「<?=$price?> 金币，成交。图纸给你——防伪起见，上面的字用 Base64 烫的，自己解。」</p>
        </div>
      </div>
    </div>
    <div class="flagline"><?=e($cipher)?></div>
    <p class="dim">F12 → Console：<code>atob("上面那串")</code>；或丢进 CyberChef 的 From Base64。解出是一句英文，口令在其中。</p>
    <p style="margin-top:14px"><a class="btn green" href="s3-forge-b55d.php">解出口令，回铁匠铺提交</a></p>
  </div>
<?php endif; ?>

</main>
<footer>WEB 新手村 · 铁匠铺柜台 | 服务端信的是订单字段，不是橱窗标价</footer>
</body>
</html>
