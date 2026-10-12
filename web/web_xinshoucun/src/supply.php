<?php
// ============================================================
//  补给站 supply.php —— 第四关实操接口
//  校验：GET key === hunter2026（凭据泄露在 map-v2.php.bak）
//  口令：trail-blazer
// ============================================================
function e($s){ return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }
$KEY = 'hunter2026';
$got = (string)($_GET['key'] ?? '');
?>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>补给站</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="topbar">
  <h1>WEB 新手村 · 村后补给站</h1>
  <div class="sub">supply.php —— 锁着的箱子，认钥匙不认人</div>
</div>
<main>

<?php if ($got === ''): ?>
  <div class="card">
    <h2>上了锁的补给箱</h2>
    <p>补给箱纹丝不动。锁孔旁边刻着一行小字：</p>
    <p class="hl">「凭 key 开箱（GET supply.php?key=...）。钥匙不发给外人和新手——问旧地图室去。」</p>
    <p class="dim">（这就是「内部接口」的感觉：知道怎么调、还知道参数，才进得来。）</p>
  </div>

<?php elseif ($got !== $KEY): ?>
  <div class="card">
    <h2>钥匙插不进去</h2>
    <p>你把 <code><?=e($got)?></code> 塞进锁孔，转了半天，纹丝不动。</p>
    <p>锁上又刻了一行小字：「v2 旧地图室的那份<b>备份</b>里有配钥匙的图纸——<b>巡守机器人</b>知道旧地图室在哪。」</p>
    <p class="dim">（提示链：/robots.txt → Disallow 的路径 → 备份源码里的 $INTERNAL_KEY。）</p>
  </div>

<?php else: ?>
  <div class="card reward">
    <h2>咔哒 · 补给箱开了</h2>
    <p>箱子里躺着一张叠得整整齐齐的<b>藏宝图</b>，边上一张纸条：</p>
    <div class="flagline">口令：trail-blazer</div>
    <p>「补给站管理员不在。留言：探险家艾拉要的东西我先放这儿了——旧地图室那把钥匙也该换了，<b>下次别再写进备份注释里了</b>。—— 临时工」</p>
    <p style="margin-top:14px"><a class="btn green" href="s4-explore-e842.php">拿口令回第四关，向艾拉提交</a></p>
  </div>
<?php endif; ?>

</main>
<footer>WEB 新手村 · 村后补给站 | 密钥写进注释的那一刻，锁就等于没了</footer>
</body>
</html>
