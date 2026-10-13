<?php
require __DIR__ . '/config.php';
?>
<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= htmlspecialchars(SITE_NAME) ?> - 主机状态监控</title>
<style>
  :root { color-scheme: light; }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: "Microsoft YaHei", "PingFang SC", "Segoe UI", sans-serif;
    background: #f4f6f8; color: #2b3440; line-height: 1.6;
  }
  .wrap { max-width: 860px; margin: 0 auto; padding: 40px 20px 60px; }
  header { display: flex; align-items: center; gap: 16px; margin-bottom: 28px; }
  .logo {
    font-size: 28px; font-weight: 700; color: #1063ff;
    border: 3px solid #1063ff; padding: 4px 10px; border-radius: 8px;
    font-family: "SimSun", serif;
  }
  header h1 { font-size: 24px; letter-spacing: 1px; }
  header small { color: #8a97a6; display: block; font-weight: 400; font-size: 13px; }
  .card {
    background: #fff; border-radius: 10px; padding: 18px 22px;
    box-shadow: 0 1px 3px rgba(16, 32, 48, .08); margin-bottom: 18px;
  }
  .card h2 { font-size: 16px; margin-bottom: 10px; color: #1c2733; }
  .notice {
    border-left: 4px solid #f0a020; background: #fffaf0;
  }
  .notice a { color: #1063ff; }
  table { width: 100%; border-collapse: collapse; font-size: 14px; }
  th, td { text-align: left; padding: 8px 10px; border-bottom: 1px solid #edf1f4; }
  th { color: #8a97a6; font-weight: 600; }
  .ok   { color: #1a9c62; }
  .warn { color: #c07a00; }
  .dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 6px; }
  .dot.ok   { background: #1a9c62; }
  .dot.warn { background: #f0a020; }
  footer { margin-top: 30px; color: #a3aeb9; font-size: 12px; text-align: center; }
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="logo">蚁</div>
    <h1><?= htmlspecialchars(SITE_NAME) ?><small>轻量级主机状态监控平台</small></h1>
  </header>

  <div class="card notice">
    <h2>维护公告 2026-10-13</h2>
    <p>核心节点升级维护中，站点已回滚至备份版本，监控数据暂停更新。
    运维同事请下载
    <a href="/backup/antcloud_backup.zip">站点备份包</a>
    自行核对配置，恢复时间另行通知。</p>
  </div>

  <div class="card">
    <h2>节点状态</h2>
    <table>
      <tr><th>节点</th><th>地域</th><th>负载</th><th>状态</th></tr>
      <tr><td>ant-01</td><td>华南 · 衡阳</td><td>31%</td><td class="ok"><span class="dot ok"></span>运行中</td></tr>
      <tr><td>ant-02</td><td>华南 · 南岳</td><td>47%</td><td class="ok"><span class="dot ok"></span>运行中</td></tr>
      <tr><td>ant-03</td><td>华东 · 湖工</td><td>--</td><td class="warn"><span class="dot warn"></span>维护中</td></tr>
    </table>
  </div>

  <div class="card">
    <h2>最近事件</h2>
    <table>
      <tr><th>时间</th><th>节点</th><th>事件</th></tr>
      <tr><td>10-13 09:12</td><td>ant-03</td><td>进入维护模式，等待升级窗口</td></tr>
      <tr><td>10-12 23:40</td><td>ant-01</td><td>例行巡检完成，一切正常</td></tr>
      <tr><td>10-11 18:05</td><td>ant-02</td><td>磁盘告警自动恢复</td></tr>
    </table>
  </div>

  <footer><?= htmlspecialchars(SITE_NAME) ?> <?= htmlspecialchars(SITE_VERSION) ?> · 蚂蚁虽小，五脏俱全</footer>
</div>
</body>
</html>
