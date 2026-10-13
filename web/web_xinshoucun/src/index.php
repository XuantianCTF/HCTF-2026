<?php
$title = '村口 · WEB 新手村';
?>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?=htmlspecialchars($title)?></title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="topbar">
  <h1>◆ WEB 新手村 ◆</h1>
  <div class="sub">WEB SECURITY · FIRST QUEST · 看见 / 对话 / 改造 / 探索 / 出剑</div>
</div>
<main>

  <div class="card">
    <h2>冒险者招募令</h2>
    <p>年轻的冒险者，欢迎来到 <span class="hl">Web 新手村</span>。</p>
    <p>村子外面游荡着名为 <span class="hl">漏洞</span> 的怪物，而你还两手空空。
    五位导师正在村里等你——他们将各送你一件<span class="ok-text">装备</span>，那是五块 flag 碎片。</p>
    <p><b>集齐五件装备，拼出出村 flag，你就是真正踏进 Web 安全之门的人。</b></p>
  </div>

  <div class="card quest">
    <h2>玩法（教考一体，30 秒看懂）</h2>
    <ol>
      <li><b>听课</b>：每关一位导师亲自教学，讲的全是本关要用的知识，不考课外内容。</li>
      <li><b>实操</b>：按任务卡亲自动手（打开 DevTools、发请求、改参数……），找到一个<span class="hl">口令</span>。口令绝不会白给，但一定是你刚学的本事能拿到的。</li>
      <li><b>领装备</b>：把口令交还给导师，获得装备（flag 碎片）和下一关地址。</li>
      <li><b>卡住了？</b>：每关底部有折叠<b>提示</b>，点开看不丢人——<span class="dim">看提示通关，也是学会。</span></li>
    </ol>
    <p class="dim">本村是教学村：允许查资料、用工具、问 AI。目标是让你带着五件装备出村，不是把你卡死在村里。</p>
  </div>

  <div class="card">
    <h2>装备架（出发前是空的）</h2>
    <div class="rack">
      <div class="slot"><div class="name">新手之眼</div><div class="code">EYES</div></div>
      <div class="slot"><div class="name">信使之声</div><div class="code">VOICE</div></div>
      <div class="slot"><div class="name">巧匠之手</div><div class="code">HANDS</div></div>
      <div class="slot"><div class="name">藏宝图</div><div class="code">MAP</div></div>
      <div class="slot"><div class="name">出村之剑</div><div class="code">SWORD</div></div>
    </div>
    <p class="dim" style="text-align:center;margin-top:10px">每通过一关点亮一件 · 五件装备词 = 出村 flag</p>
  </div>

  <div style="text-align:center;margin:26px 0 10px">
    <a class="btn green" href="s1-look-f3a9.php">进入第一关：看见（Look）</a>
  </div>

</main>
<footer>WEB 新手村 · 村委会教务处 出品 | 教学村规则：只教不坑，卡住就看提示</footer>
</body>
</html>
