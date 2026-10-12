<?php
// ============================================================
//  第二关 · 对话（SPEAK）—— 考点：HTTP 报文 / User-Agent /
//  Referer / curl 构造请求
//  口令：say-hello（由 messenger.php 校验 UA + Referer 后发放）
// ============================================================
$PASS = 'say-hello';
$passed = false; $err = '';
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
    $got = strtolower(trim((string)($_POST['pass'] ?? '')));
    if ($got === $PASS) { $passed = true; }
    else { $err = '梅琳摇摇头：「这不是驿站回执上的口令。去 messenger.php 问问看——记得带上你的『名片』。」'; }
}
function e($s){ return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }
?>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>第二关 · 对话 SPEAK</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="topbar">
  <h1>WEB 新手村 · 第二关</h1>
  <div class="sub">对话 SPEAK —— 别让浏览器替你说话，学会直接和服务器对话</div>
  <div class="dots"><span class="on">●</span><span class="now">●</span><span class="off">○</span><span class="off">○</span><span class="off">○</span><span class="off">○</span></div>
</div>
<main>

  <div class="card">
    <div class="npc">
      <div class="avatar">信</div>
      <div>
        <div class="who">驿站站长 · 梅琳</div>
        <div class="bubble">
          <p>老兵教你看，我教你<b>说</b>。</p>
          <p>你每打开一个网页，其实是浏览器替你向服务器寄了一封<b>信</b>（HTTP 请求）。信里除了正文，还有<b>信头</b>——你的名片：你是谁（User-Agent）、你从哪来（Referer）。</p>
          <p>浏览器替你写名片，你便做不了主。<b>学会自己写信，你才算真正会「上网」。</b></p>
        </div>
      </div>
    </div>
  </div>

  <div class="card">
    <h2>第二课 · 一封 HTTP 信长什么样</h2>
    <p>你在地址栏敲下网址回车，浏览器寄出的信大致长这样（原始报文）：</p>
<pre>GET /index.php HTTP/1.1          ← 请求行：方法 路径 协议
Host: village.example.com        ← 我要找谁
User-Agent: Mozilla/5.0 ...      ← 名片：我是谁（用什么工具发的请求）
Referer: http://xxx/prev.html    ← 名片：我从哪个页面跳过来的
                                 ← （空行：信头结束，下面是正文）
（GET 请求一般没有正文；POST 的表单数据放在这里）</pre>
    <p>服务器回信也带信头：<b>状态码</b>（200 成功 / 302 跳转 / 403 禁止 / 404 没这页）和 <b>Set-Cookie</b> 等等。第五关会用到。</p>

    <h3>curl：命令行里的「寄信工具」</h3>
    <p>curl 是最经典的 HTTP 客户端，Windows 10+ 自带（cmd / PowerShell 直接用）。三个本关必会用法：</p>
<pre># 1. 寄一封普通的信（GET 请求）
curl http://&lt;服务地址&gt;/index.php

# 2. 换一张名片（自定义 User-Agent）
curl -A "MyAgent/1.0" http://&lt;服务地址&gt;/index.php

# 3. 自定义任意请求头（如 Referer）
curl -H "Referer: https://example.com/" http://&lt;服务地址&gt;/index.php</pre>
    <p class="dim">「服务地址」就是你浏览器地址栏里看到的村子地址（本地自建如 127.0.0.1:8023，比赛环境用题目给的目标）。-A 和 -H 可以同一条命令一起用。</p>
  </div>

<?php if ($passed): ?>
  <div class="card reward">
    <h2>通关！梅琳笑纳：「这封信，写得漂亮。」</h2>
    <div class="equip">
      <div class="glyph">信</div>
      <div class="name">信使之声 · VOICE</div>
      <div class="code">VOICE</div>
    </div>
    <p>从此你不再假手浏览器——请求行、请求头，皆由你亲笔。这是 flag 的第二块碎片。</p>
    <div class="flagline">碎片 2 / 5 ：VOICE</div>
    <p class="dim">把装备词记下来，毕业门要集齐五件。</p>
    <p style="margin-top:16px"><a class="btn green" href="s3-forge-b55d.php">前往第三关：改造（MODIFY）</a></p>
  </div>
<?php else: ?>
  <div class="card quest">
    <h2>任务 · 只接待信使的驿站柜台</h2>
    <p class="goal">驿站内部柜台 <code>messenger.php</code> 掌握着本关口令，但它<b>只接待真正的信使</b>，规矩有两条：</p>
    <ul>
      <li>名片上的身份必须是 <code>RookieCourier/1.0</code>（User-Agent，一字不差）。</li>
      <li>必须携带<b>长老会</b>抬头的介绍信：<code>Referer: https://elders.village.gov/</code>（同样一字不差）。</li>
    </ul>
    <p>用浏览器直接点进去只会吃闭门羹——柜台会看你的「名片」决定说什么。<b>它的每句拒绝都是线索。</b></p>
    <p><a class="btn ghost" href="messenger.php">先去柜台碰碰运气</a></p>
    <form method="post" class="gate">
      <input type="text" name="pass" placeholder="输入驿站回执上的口令" autocomplete="off">
      <button class="btn" type="submit">向梅琳提交</button>
    </form>
    <?php if ($err): ?><div class="err-box"><?=e($err)?></div><?php endif; ?>
  </div>

  <div class="card">
    <h2>卡住了？看提示</h2>
    <details class="hint">
      <summary>提示一：方向</summary>
      <div class="hint-body">浏览器不方便自定义 User-Agent 和 Referer——这正是第二课存在的意义：用 <b>curl</b> 来「寄信」。柜台缺什么，报错信息会告诉你；缺什么就补什么。</div>
    </details>
    <details class="hint">
      <summary>提示二：具体命令</summary>
      <div class="hint-body">
        <p>把两个名片要求合在同一条 curl 里（服务地址按实际目标替换）：</p>
        <pre>curl -A "RookieCourier/1.0" -H "Referer: https://elders.village.gov/" http://&lt;服务地址&gt;/messenger.php</pre>
      </div>
    </details>
  </div>
<?php endif; ?>

</main>
<footer>WEB 新手村 · 第二关 对话 | 服务器的报错不是冷遇，是它在你耳边递话</footer>
</body>
</html>
