<?php
// ============================================================
//  第四关 · 探索（EXPLORE）—— 考点：robots.txt / 备份文件泄露 /
//  源码泄露（密钥与内部接口）
//  链路：/robots.txt → /map-v2.php.bak（读源码得 key）
//        → /supply.php?key=hunter2026 → 口令 trail-blazer
// ============================================================
$PASS = 'trail-blazer';
$passed = false; $err = '';
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
    $got = strtolower(trim((string)($_POST['pass'] ?? '')));
    if ($got === $PASS) { $passed = true; }
    else { $err = '艾拉盯着地图：「补给站在旧地图室后面——先去问问巡守机器人，再翻翻备份。」'; }
}
function e($s){ return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }
?>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>第四关 · 探索 EXPLORE</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="topbar">
  <h1>WEB 新手村 · 第四关</h1>
  <div class="sub">探索 EXPLORE —— 网站没告诉你的地方，才是它真正的全貌</div>
  <div class="dots"><span class="on">●</span><span class="on">●</span><span class="on">●</span><span class="now">●</span><span class="off">○</span><span class="off">○</span></div>
</div>
<main>

  <div class="card">
    <div class="npc">
      <div class="avatar">探</div>
      <div>
        <div class="who">探险家 · 艾拉</div>
        <div class="bubble">
          <p>前三位教的都是「页面之内」的本事。我带你找<b>页面之外</b>的东西。</p>
          <p>一个网站除了你能点到的链接，还有一堆「存在、但没写进菜单」的角落：说明文件、旧备份、忘了删的接口……<b>探险家的第一课：「禁止入内」的牌子，就是路标。</b></p>
        </div>
      </div>
    </div>
  </div>

  <div class="card">
    <h2>第四课 · 三处必翻的角落</h2>

    <h3>1. robots.txt —— 站长写给爬虫的「此地无银」清单</h3>
    <p>几乎所有网站根目录都有一个 <code>/robots.txt</code>，站长在里面告诉搜索引擎「<b>这些路径不要收录、不要进去</b>」：</p>
<pre>User-agent: *          # 对所有爬虫说
Disallow: /admin/      # 这个目录别进！
Disallow: /secret.txt  # 这个文件别看！</pre>
    <p>问题是：爬虫会守规矩，<b>人不会</b>。对探险家来说，Disallow 列表就是一张藏宝图。访问方式：地址栏直接敲 <code>http://站点/robots.txt</code>。</p>

    <h3>2. 备份文件 —— 改稿留下的影子</h3>
    <p>开发者改代码时，常在服务器上留下 <code>xxx.php.bak</code>、<code>.old</code>、<code>.swp</code>、<code>xxx.zip</code> 之类的旧文件。
    网页从不链接它们，但只要知道文件名就能直接访问。最要命的是：<b>.bak 不会被当成 PHP 执行，而是当成纯文本原样吐出来——等于把源代码送你手上</b>。</p>
    <p class="dim">浏览器可能提示「下载文件」——用记事本 / VSCode 打开即可，这是正常现象。</p>

    <h3>3. 源码泄露 —— 拿到源码 = 拿到逻辑</h3>
    <p>源码里常躺着不该见光的东西：密钥、账号、内部接口的调用方式。读懂它，就能照着「钥匙孔」把门叫开。</p>
    <p class="dim">进阶预告：还有工具能拿字典批量猜文件名和目录（dirsearch 等），出村后你会遇见它们。</p>
  </div>

<?php if ($passed): ?>
  <div class="card reward">
    <h2>通关！艾拉大笑：「『禁止入内』四个字，你读成『欢迎光临』了。」</h2>
    <div class="equip">
      <div class="glyph">探</div>
      <div class="name">藏宝图 · MAP</div>
      <div class="code">MAP</div>
    </div>
    <p>robots、备份、源码——从此没有「找不到」，只有「还没找」。这是 flag 的第四块碎片。</p>
    <div class="flagline">碎片 4 / 5 ：MAP</div>
    <p class="dim">最后一件装备在村公所，出村之门就在眼前。</p>
    <p style="margin-top:16px"><a class="btn green" href="s5-hit-d19c.php">前往第五关：出剑（HIT）</a></p>
  </div>
<?php else: ?>
  <div class="card quest">
    <h2>任务 · 补给站的钥匙</h2>
    <p class="goal">村后的<b>补给站</b>（<code>supply.php</code>）里锁着本关口令。开锁的钥匙没写在任何页面上——但这个村子到处是「不该看的地方」：</p>
    <ul>
      <li>第一步永远免费：去读本村的 <code>robots.txt</code>（就在站点根目录，地址栏直接访问）。</li>
      <li>巡守机器人「禁止」你去的地方，就是你要去的地方。那儿躺着一份<b>旧文件的备份</b>。</li>
      <li>备份里的源码会告诉你：钥匙是什么、补给站怎么开。</li>
    </ul>
    <form method="post" class="gate">
      <input type="text" name="pass" placeholder="输入补给站取出的口令" autocomplete="off">
      <button class="btn" type="submit">向艾拉提交</button>
    </form>
    <?php if ($err): ?><div class="err-box"><?=e($err)?></div><?php endif; ?>
  </div>

  <div class="card">
    <h2>卡住了？看提示</h2>
    <details class="hint">
      <summary>提示一：方向</summary>
      <div class="hint-body">地址栏访问 <code>http://&lt;服务地址&gt;/robots.txt</code>，把 Disallow 的路径原样拼到站点地址后面访问。读到备份源码后，逐行找：<b>像钥匙的字符串</b>和<b>怎么用它调接口</b>，注释里都写了。</div>
    </details>
    <details class="hint">
      <summary>提示二：具体操作</summary>
      <div class="hint-body">
        <p>1. 打开 <code>/robots.txt</code>，记下 Disallow 后面的路径，访问之（可能是下载文件，用记事本打开）。</p>
        <p>2. 源码里找到 <code>$INTERNAL_KEY</code> 和补给接口的用法说明，然后：</p>
        <pre>curl "http://&lt;服务地址&gt;/supply.php?key=你找到的钥匙"</pre>
        <p>（浏览器地址栏直接拼 URL 访问也一样——这是个 GET 接口。）</p>
      </div>
    </details>
  </div>
<?php endif; ?>

</main>
<footer>WEB 新手村 · 第四关 探索 | Disallow 是站长画给守规矩者的边界</footer>
</body>
</html>
