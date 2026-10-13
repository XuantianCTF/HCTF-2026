<?php
// ============================================================
//  第三关 · 改造（MODIFY）—— 考点：表单结构 / hidden 字段篡改 /
//  前端校验绕过 / Base64 解码
//  口令：smith-hand（forge.php 校验价格后返回 Base64 密文，
//  玩家解码获得）
// ============================================================
$PASS = 'smith-hand';
$passed = false; $err = '';
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
    $got = strtolower(trim((string)($_POST['pass'] ?? '')));
    if ($got === $PASS) { $passed = true; }
    else { $err = '布洛克挠挠头：「口令在图纸密文里，得先把图纸买下来、解开再说。」'; }
}
function e($s){ return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }
?>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>第三关 · 改造 MODIFY</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="topbar">
  <h1>WEB 新手村 · 第三关</h1>
  <div class="sub">改造 MODIFY —— 页面上的一切数据，出发前都要经过你的手</div>
  <div class="dots"><span class="on">●</span><span class="on">●</span><span class="now">●</span><span class="off">○</span><span class="off">○</span><span class="off">○</span></div>
</div>
<main>

  <div class="card">
    <div class="npc">
      <div class="avatar">匠</div>
      <div>
        <div class="who">铁匠 · 布洛克</div>
        <div class="bubble">
          <p>梅琳教你说话，我教你<b>改口</b>。</p>
          <p>网页上每一个输入框、每一个按钮、每一个「看不见」的数值——送到服务器之前，<b>都要先经过你的电脑</b>。你的地盘，你做主。</p>
        </div>
      </div>
    </div>
  </div>

  <div class="card">
    <h2>第三课 · 表单的解剖与三样本事</h2>

    <h3>1. 表单：页面向服务器「递单子」的方式</h3>
<pre>&lt;form method="POST" action="forge.php"&gt;   &lt;!-- 单子递到哪个柜台、用什么方式 --&gt;
  &lt;input type="text" name="price" value="100"&gt;  &lt;!-- name=参数名，value=值 --&gt;
  &lt;input type="hidden" name="token" value="x"&gt;  &lt;!-- 隐藏字段：页面上看不见 --&gt;
  &lt;button type="submit"&gt;提交&lt;/button&gt;
&lt;/form&gt;</pre>
    <p><b>hidden（隐藏）字段</b>只是「页面上不显示」，它照样跟着表单发给服务器。
    而你在 F12 → Elements 里双击任何 <code>value</code>，都可以<b>当场改掉它</b>——看不见，不等于改不了。</p>

    <h3>2. 前端校验：门口的保安，不是金库的锁</h3>
    <p>很多网站用 JS 在浏览器里先检查一遍（比如「余额不足不许提交」）。
    但浏览器是<b>你的</b>：JS 校验可以禁用、可以改价格后自然通过、也可以干脆绕开页面直接用 curl 递单子（第二课的功夫）。
    <b>真正靠谱的校验必须在服务器端</b>——这句话现在不懂没关系，先记住。</p>

    <h3>3. Base64：Web 世界最常见的「障眼法」</h3>
    <p>由 <code>A-Z a-z 0-9 + /</code> 组成、结尾常带一两个 <code>=</code> 的一串字符，八成就是 Base64。它不是加密，只是「换了种写法」，人人可逆。</p>
    <p>F12 → Console 里就能解：</p>
<pre>&gt; atob("aGVsbG8gdmlsbGFnZQ==")   // 解码
&lt; "hello village"
&gt; btoa("hello village")          // 编码（反向）</pre>
    <p class="dim">也可以用 CyberChef（在线工具）或命令行。Base64 解出来的中文在某些工具里会乱码，英文则一定正常。</p>
  </div>

<?php if ($passed): ?>
  <div class="card reward">
    <h2>通关！布洛克咧嘴一笑：「好手艺，价钱谈得漂亮。」</h2>
    <div class="equip">
      <div class="glyph">匠</div>
      <div class="name">巧匠之手 · HANDS</div>
      <div class="code">HANDS</div>
    </div>
    <p>从此表单里没有你递不出的数据：hidden 可改、前端校验可绕、Base64 可解。这是 flag 的第三块碎片。</p>
    <div class="flagline">碎片 3 / 5 ：HANDS</div>
    <p class="dim">装备词记好，毕业门集齐五件。</p>
    <p style="margin-top:16px"><a class="btn green" href="s4-explore-e842.php">前往第四关：探索（EXPLORE）</a></p>
  </div>
<?php else: ?>
  <div class="card quest">
    <h2>任务 · 铁匠铺的亏本买卖</h2>
    <table class="grid">
      <tr><th>商品</th><th>价格</th><th>你的钱包</th></tr>
      <tr><td>出村之剑锻造图（含本关口令）</td><td><span class="hl">100 金币</span></td><td><span class="ok-text">10 金币</span></td></tr>
    </table>
    <p class="goal">把「出村之剑锻造图」买下来。图纸上的口令用 Base64 写成密文（铁匠管这叫防伪），解码即得。</p>
    <ul>
      <li>柜台只认<b>订单上写的价格</b>（表单里的 <code>price</code> 字段），不认橱窗标价牌。</li>
      <li>店里那台「验钞机」（前端 JS 校验）只装在门口——它说不行，不代表柜台说不行。</li>
      <li>铁匠的底线：不赊账、不白送（价格须 ≥ 1），也绝不亏本收超过钱包的钱。</li>
    </ul>
    <pre>当前订单（本页源码 / Elements 里可见可改）：
  item  = sword-blueprint
  price = 100</pre>
    <form method="post" action="forge.php" onsubmit="return checkOrder(this);">
      <input type="hidden" name="item" value="sword-blueprint">
      <input type="hidden" name="price" value="100">
      <button class="btn" type="submit">支付购买</button>
    </form>
    <p class="dim">点一下试试也无妨——被拦住了，正好看看「验钞机」长什么样（右键查看源代码，或读本页 JS）。</p>
    <form method="post" class="gate">
      <input type="text" name="pass" placeholder="输入图纸密文里的口令" autocomplete="off">
      <button class="btn" type="submit">向布洛克提交</button>
    </form>
    <?php if ($err): ?><div class="err-box"><?=e($err)?></div><?php endif; ?>
  </div>

  <div class="card">
    <h2>卡住了？看提示</h2>
    <details class="hint">
      <summary>提示一：方向</summary>
      <div class="hint-body">「验钞机」只是门口的 JS：<code>onsubmit</code> 时对比订单价格和钱包。路有三条——F12 里把订单上 <code>price</code> 的 value 改成钱包付得起的数；或改完用页面正常提交；或干脆用 curl 直接向 <code>forge.php</code> 递一张价格合理的 POST 单子（第二课的功夫又用上了）。</div>
    </details>
    <details class="hint">
      <summary>提示二：具体命令</summary>
      <div class="hint-body">
        <pre>curl -X POST -d "item=sword-blueprint&amp;price=10" http://&lt;服务地址&gt;/forge.php</pre>
        <p>买成后页面会给一串 Base64 密文。F12 → Console 执行 <code>atob("那串密文")</code>，口令就在解出的英文句子里。</p>
      </div>
    </details>
  </div>
<?php endif; ?>

</main>
<footer>WEB 新手村 · 第三关 改造 | 看不见的字段不是锁，只是帘子</footer>
<script>
// 铁匠铺「验钞机」——纯前端校验，装在门口的摆设。
// 想绕过它？它读的正是订单上的 price，而这个值……你说了算。
function checkOrder(f) {
  var price = parseInt(f.price.value, 10);
  var wallet = 10; // 你钱包里的金币
  if (isNaN(price) || price > wallet) {
    alert('【验钞机】叮——！金币不足：需 ' + price + '，钱包只有 ' + wallet + '。\n本店概不赊账！');
    return false; // 拦住表单，不递给柜台
  }
  return true;
}
</script>
</body>
</html>
