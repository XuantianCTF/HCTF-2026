<?php
// ============================================================
//  毕业门 graduate-a67f.php —— 集齐五件装备，拼出出村 flag
//  EYES / VOICE / HANDS / MAP / SWORD
//  最终 flag 动态注入：读 FLAG 环境变量（平台部署），
//  未注入时回退默认值（保持 hctf{} 格式）。
// ============================================================
$FLAG = getenv('FLAG') ?: 'hctf{EYES_VOICE_HANDS_MAP_SWORD}';
$EXPECT = [
    1 => ['code' => 'EYES',  'label' => '装备一 · 新手之眼（第一关）'],
    2 => ['code' => 'VOICE', 'label' => '装备二 · 信使之声（第二关）'],
    3 => ['code' => 'HANDS', 'label' => '装备三 · 巧匠之手（第三关）'],
    4 => ['code' => 'MAP',   'label' => '装备四 · 藏宝图（第四关）'],
    5 => ['code' => 'SWORD', 'label' => '装备五 · 出村之剑（第五关）'],
];
$results = null;
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
    $results = [];
    foreach ($EXPECT as $i => $meta) {
        $got = strtoupper(trim((string)($_POST['e'.$i] ?? '')));
        $results[$i] = ($got === $meta['code']);
    }
}
$allOk = is_array($results) && !in_array(false, $results, true);
function e($s){ return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }
?>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>毕业门 · 出村</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="topbar">
  <h1>WEB 新手村 · 毕业门</h1>
  <div class="sub">GRADUATE —— 把五件装备依次挂上门楣，门自会开</div>
  <div class="dots"><span class="on">●</span><span class="on">●</span><span class="on">●</span><span class="on">●</span><span class="on">●</span><span class="now">●</span></div>
</div>
<main>

<?php if ($allOk): ?>
  <div class="card reward">
    <h2>门开了 —— 恭喜出村，冒险者！</h2>
    <p>五件装备依次归位，石门轰然中开。门后的石碑上，刻着属于你的出村凭证：</p>
    <div class="final-flag"><?=e($FLAG)?></div>
    <p class="dim" style="text-align:center">五个装备词 EYES_VOICE_HANDS_MAP_SWORD 是你一路走来的路标；石碑上的凭证，才是村外世界认的 flag。</p>

    <div class="cert">
      <div class="big">出 村 证 书</div>
      <p>兹证明 <b>无名新手</b> 于 WEB 新手村完成全部训练，掌握五项基本技能：</p>
      <p>看见（源码与 DOM）· 对话（HTTP 与 curl）· 改造（表单与编码）· 探索（信息收集）· 出剑（越权与逻辑）</p>
      <p class="hl">特此出村，前途无量。</p>
      <p class="dim">—— WEB 新手村村委会 · 五位导师 联合签发</p>
    </div>

    <div class="card" style="margin-top:22px">
      <h2>三条毕业箴言（出村前请收好）</h2>
      <ol>
        <li><b>客户端的一切都不可信。</b>页面上的校验、隐藏字段、显示的价格——送到服务器之前都经过用户之手，真正的防线必须建在服务端。</li>
        <li><b>一切输入皆攻击面。</b>参数、请求头、Cookie、URL 路径……你今天改过的每一种输入，都可以是下一场战斗的突破口。</li>
        <li><b>四问。</b>面对任何接口问四句：数据从哪来？到哪去？谁校验它？校验在哪一端？——答案里藏着漏洞。</li>
      </ol>
    </div>

    <div class="card">
      <h2>下一站（出村路线图）</h2>
      <ul>
        <li><b>SQL 注入</b>：万能密码 <code>' or 1=1 -- </code> 的世界，数据库在向你招手。</li>
        <li><b>XSS</b>：让别人的浏览器替你跑 JS。顺便一提——本村所有玩家输入都做了 <code>htmlspecialchars</code> 转义，等你学了 XSS 就知道为什么了。</li>
        <li><b>Burp Suite</b>：比 curl 更顺手的全能瑞士军刀，抓包、改包、重放。</li>
        <li><b>练手平台</b>：BUUCTF、攻防世界、CTFHub 的 Web 新手区，正好接住你今天学会的一切。</li>
      </ul>
      <p class="dim">村民闲聊还记得吗？「禁止进入」读作「欢迎光临」——从今天起，这句话由你来实践了。</p>
    </div>
  </div>

<?php else: ?>
  <div class="card quest">
    <h2>毕业门 · 装备归位</h2>
    <p class="goal">门楣上有五个凹槽。把五件装备的<b>装备词</b>（每关通关时导师发你的那个英文词）依次填入：</p>
    <form method="post">
      <table class="grid">
        <tr><th>凹槽</th><th>装备词</th><th style="width:90px">状态</th></tr>
        <?php foreach ($EXPECT as $i => $meta): ?>
        <tr>
          <td><?=e($meta['label'])?></td>
          <td><input type="text" name="e<?=$i?>" placeholder="第 <?=$i?> 关所得装备词"
                     value="<?=e($_POST['e'.$i] ?? '')?>" style="width:100%;font-family:inherit;font-size:14px;background:#0a0d1c;color:#e8ecff;border:2px solid #2c3358;padding:6px 8px;"></td>
          <td>
            <?php if (is_array($results)): ?>
              <?= $results[$i] ? '<span class="ok-text">√ 已点亮</span>' : '<span class="err-text">×</span>' ?>
            <?php else: ?>
              <span class="dim">待放入</span>
            <?php endif; ?>
          </td>
        </tr>
        <?php endforeach; ?>
      </table>
      <p><button class="btn" type="submit">转动门轮</button></p>
    </form>
    <?php if (is_array($results) && !$allOk): ?>
      <div class="err-box">门轮卡住了一声。哪个凹槽亮着「×」，就回哪一关找导师——通关时发你的装备词都写在「碎片 N/5」的横幅上。</div>
    <?php endif; ?>
    <details class="hint">
      <summary>装备词忘了 / 没记？</summary>
      <div class="hint-body">每关的装备词都出现在通关奖励卡的 <b>「碎片 N / 5 ：XXXX」</b> 横幅上，以及装备卡下半部分的大写英文词。丢了就得回关卡重拿一次口令——好消息是：你现在应该两分钟就能通关一次了。</div>
    </details>
  </div>
<?php endif; ?>

</main>
<footer>WEB 新手村 · 毕业门 | 出村不是结束，是你自己名字的开始</footer>
</body>
</html>
