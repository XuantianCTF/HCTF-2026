<?php
// ============================================================
//  第一关 · 看见（LOOK）—— 考点：查看源代码 / DevTools / HTML 注释
//  / display:none / JS 动态 DOM
//  口令：eyes-open（藏在 village.js 动态插入的隐藏告示牌里，
//  页面源码注释负责引导玩家去 Elements 找）
// ============================================================
$PASS = 'eyes-open';
$passed = false; $err = '';
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
    $got = strtolower(trim((string)($_POST['pass'] ?? '')));
    if ($got === $PASS) { $passed = true; }
    else { $err = '老兵眯起独眼：「这不是告示牌上的口令。再找找——记得我教你的本事。」'; }
}
function e($s){ return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }
?>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>第一关 · 看见 LOOK</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="topbar">
  <h1>WEB 新手村 · 第一关</h1>
  <div class="sub">看见 LOOK —— 浏览器给你看的，不等于服务器给你的全部</div>
  <div class="dots"><span class="now">●</span><span class="off">○</span><span class="off">○</span><span class="off">○</span><span class="off">○</span><span class="off">○</span></div>
</div>
<main>

  <!-- ================================================================ -->
  <!-- [独眼老兵·凯恩] 能翻到这段注释，说明你已经会用「查看源代码」了。 -->
  <!--   不错，第一步成了。                                              -->
  <!--   不过村口的告示牌不是我立的——是村民每天用 JS 重新挂上去的，     -->
  <!--   还罩了一层 display:none 的「隐形魔法」：                       -->
  <!--   「查看源代码」里翻不到它（源码是服务器发来的原始 HTML），       -->
  <!--   但在 Elements 的实时 DOM 里，它无所遁形。                      -->
  <!--   按 F12 → Elements，Ctrl+F 搜一搜：notice-board                 -->
  <!-- ================================================================ -->

  <div class="card">
    <div class="npc">
      <div class="avatar">眼</div>
      <div>
        <div class="who">独眼老兵 · 凯恩</div>
        <div class="bubble">
          <p>年轻人，在 Web 的世界里，<b>你眼睛看到的页面，只是浏览器想让你看到的</b>。</p>
          <p>真相藏在两样东西里——听好了，我只讲一遍：</p>
        </div>
      </div>
    </div>
  </div>

  <div class="card">
    <h2>第一课 · 两双眼睛</h2>
    <h3>1. 查看源代码（Ctrl + U）—— 服务器发来的「原始 HTML」</h3>
    <p>在任何网页上按 <code>Ctrl + U</code>，你看到的就是服务器原样发来的 HTML 文本。
    页面作者写的<b>注释</b>也会原样躺在里面——注释是给人看的备注，浏览器不显示它：</p>
    <pre>&lt;!-- 这是一条 HTML 注释：页面上看不见，源代码里看得见 --&gt;</pre>
    <p class="dim">出题人忘记删注释、把秘密写进注释里，是 Web 安全最经典的「入门第一杀」。你现在就可以在本页源码里试试。</p>

    <h3>2. 开发者工具（F12）—— 浏览器的「实时透视镜」</h3>
    <p>按 <code>F12</code> 打开 DevTools，最常用的是这三个面板：</p>
    <ul>
      <li><b>Elements</b>：实时 DOM 树——页面<b>此刻真实的样子</b>。JS 改过的、用 <code>display:none</code> 藏起来的元素，全在这里。支持 <code>Ctrl + F</code> 搜索。</li>
      <li><b>Network</b>：页面加载时发出的<b>每一个请求</b>（HTML、JS、图片、接口……）。</li>
      <li><b>Console</b>：可以执行 JS 的控制台，后面关卡会用到。</li>
    </ul>
    <p><b>关键区别</b>：「查看源代码」是服务器发来的<b>原始底稿</b>；Elements 是浏览器跑完 JS 之后的<b>现场</b>。
    JS 动态添加的元素，源代码里没有，Elements 里才有。</p>
  </div>

<?php if ($passed): ?>
  <div class="card reward">
    <h2>通关！老兵把独眼一瞪：「好眼力。」</h2>
    <div class="equip">
      <div class="glyph">眼</div>
      <div class="name">新手之眼 · EYES</div>
      <div class="code">EYES</div>
    </div>
    <p>从此你能看见别人看不见的东西——注释、隐藏元素、真实 DOM。这是冒险者第一件装备，也是 <b>flag 的第一块碎片</b>。</p>
    <div class="flagline">碎片 1 / 5 ：EYES</div>
    <p class="dim">把装备词记在冒险手册上（截图也行），出村的毕业门要用。</p>
    <p style="margin-top:16px"><a class="btn green" href="s2-speak-7c21.php">前往第二关：对话（SPEAK）</a></p>
  </div>
<?php else: ?>
  <div class="card quest">
    <h2>任务 · 隐形的告示牌</h2>
    <p class="goal">村口有一块「隐形告示牌」，上面写着本关口令。把它找出来，向老兵报到。</p>
    <ul>
      <li>告示牌被 <code>display:none</code> 的隐形魔法罩着，<b>页面上看不见</b>。</li>
      <li>它是村民用 JS 每天重新挂上去的，所以「查看源代码」里也<b>翻不到</b>。</li>
      <li>老兵在<b>本页源代码的注释里</b>留了话，指点你怎么找。（先按 Ctrl+U 看看？）</li>
    </ul>
    <form method="post" class="gate">
      <input type="text" name="pass" placeholder="输入告示牌上的口令" autocomplete="off" autofocus>
      <button class="btn" type="submit">向老兵报到</button>
    </form>
    <?php if ($err): ?><div class="err-box"><?=e($err)?></div><?php endif; ?>
  </div>

  <div class="card">
    <h2>卡住了？看提示</h2>
    <details class="hint">
      <summary>提示一：方向</summary>
      <div class="hint-body">按 <code>F12</code> 打开 DevTools，切到 <b>Elements</b> 面板，按 <code>Ctrl + F</code> 搜索 <code>notice-board</code>。被隐形魔法罩住的告示牌，在实时 DOM 里看得一清二楚。</div>
    </details>
    <details class="hint">
      <summary>提示二：具体操作</summary>
      <div class="hint-body">
        <p>F12 → Elements → Ctrl+F 搜 <code>notice-board</code> → 双击定位到那个 <code>div</code>。口令就写在它的文字内容里。</p>
        <p>另一种殊途同归的路：F12 → <b>Network</b>（或 Sources）面板，找到本页加载的 <code>village.js</code>，点开读它的源码——口令的「出生地」就在那里。</p>
      </div>
    </details>
  </div>
<?php endif; ?>

  <div class="chat-slot"></div>
</main>
<footer>WEB 新手村 · 第一关 看见 | 卡住不丢人，不看提示才是跟自己怄气</footer>
<script src="village.js"></script>
</body>
</html>
