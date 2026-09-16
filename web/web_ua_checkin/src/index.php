<?php
$PRANK_URL = 'https://www.bilibili.com/video/BV1sa4y1X7Ng/?share_source=copy_web&t=16';

$ua = $_SERVER['HTTP_USER_AGENT'] ?? '';
$isiPhone = (bool)preg_match('/iPhone/i', $ua);

if (!$isiPhone) {
    header('Location: ' . $PRANK_URL, true, 302);
    exit;
}
?>
<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="format-detection" content="telephone=no">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black">
<title>Only iPhone</title>
<!--
  ============================================================
  求你们不要再嘲笑这些题目了
  这个题目是我花了好多token想的 QWQ
  ============================================================
  <?php echo base64_encode(getenv('FLAG') ?: 'hctf{S0urc3_C0d3_D0esnt_L1e}') . "\n"; ?>
-->
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html, body { height: 100%; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "PingFang SC", "Helvetica Neue", "Microsoft YaHei", sans-serif;
    background: #000;
    color: #F5F5F7;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 48px 28px;
    -webkit-font-smoothing: antialiased;
    text-align: center;
  }
  .poster { max-width: 560px; }
  .logo { width: 44px; height: 54px; fill: #F5F5F7; opacity: .92; }
  h1 {
    margin-top: 36px;
    font-size: 56px;
    line-height: 1.08;
    font-weight: 700;
    letter-spacing: -.02em;
    color: #F5F5F7;
  }
  .sub {
    margin-top: 20px;
    font-size: 28px;
    font-weight: 600;
    color: #F5F5F7;
  }
  .desc {
    margin-top: 26px;
    font-size: 17px;
    line-height: 1.65;
    color: #86868B;
  }
  .cta {
    display: inline-block;
    margin-top: 38px;
    padding: 14px 34px;
    border-radius: 980px;
    background: #0071E3;
    color: #F5F5F7;
    font-size: 17px;
    font-weight: 400;
    text-decoration: none;
    cursor: pointer;
    -webkit-tap-highlight-color: transparent;
  }
  .cta:active { background: #0062C4; }
  .note {
    position: fixed;
    left: 0;
    right: 0;
    bottom: 18px;
    text-align: center;
    font-size: 12px;
    color: #48484A;
    line-height: 1.6;
  }
</style>
</head>
<body>
<main class="poster">
  <svg class="logo" viewBox="0 0 814 1000" aria-hidden="true"><path d="M788.1 340.9c-5.8 4.5-108.2 62.2-108.2 190.5 0 148.4 130.3 200.9 134.2 202.2-.6 3.2-20.7 71.9-68.7 141.9-42.8 61.6-87.5 123.1-155.5 123.1s-85.5-39.5-164-39.5c-76.5 0-103.7 40.8-165.9 40.8s-105.6-57-155.5-127C46.7 790.7 0 663 0 541.8c0-194.4 126.4-297.5 250.8-297.5 66.1 0 121.2 43.4 162.7 43.4 39.5 0 101.1-46 176.3-46 28.5 0 130.9 2.6 198.3 99.2zm-234-181.5c31.1-36.9 53.1-88.1 53.1-139.3 0-7.1-.6-14.3-1.9-20.1-50.6 1.9-110.8 33.7-147.1 75.8-28.5 32.4-55.1 83.6-55.1 135.5 0 7.8 1.3 15.6 1.9 18.1 3.2.6 8.4 1.3 13.6 1.3 45.4 0 102.5-30.4 135.5-71.3z"/></svg>
  <h1>Only iPhone can do.</h1>
  <p class="desc">尊贵的iPhone用户，这份flag为你呈上，点击即可获得</p>
  <a class="cta" href="https://www.apple.com.cn/">马上获得</a>
</main>
<p class="note">兼容性：Android、iPad 及桌面设备均不受支持。<br>© 2026</p>
</body>
</html>
