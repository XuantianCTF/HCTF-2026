# web_ua_checkin —— Web 签到题（PHP 版 · Only iPhone）出题人文档

> 玩家不可见本文档。改编自原签到题 ua-checkin（PHP 版），本版是其 HCTF-2026
> 规范化版本：flag 由硬编码改为平台动态注入，并由白盒改为**黑盒**（不发布
> 源码附件，选手仅有线上靶机地址），UA 分流逻辑、整蛊跳转与页面玩梗文案
> （"求你们不要再嘲笑这些题目了 QWQ"、Only iPhone 梗）零改动。

模仿真实钓鱼站 cloaking（UA 差异化响应）手法的签到题，服务端分流，玩库克 "Only iPhone can do" 梗。

## Flag 约定（HCTF-2026 全场统一）

- **真 flag**：`hctf{}` 包裹，**动态**——`index.php` 渲染 HTML 注释时执行

  ```php
  base64_encode(getenv('FLAG') ?: 'hctf{S0urc3_C0d3_D0esnt_L1e}')
  ```

  由 ret2shell 平台在容器启动时注入 `FLAG` 环境变量；未注入时回退默认值
  `hctf{S0urc3_C0d3_D0esnt_L1e}`（保持 `hctf{}` 格式，静态部署可直接使用）。
  考点不变：flag 仍是 iPhone 分支页面注释里的一段 base64，只是改为运行时生成。
- 本题**无蜜罐/假 flag**，不使用 `fflag{}`
- 原题真 flag 为 `flag{S0urc3_C0d3_D0esnt_L1e}`（base64 硬编码于注释），
  改造时仅更换包裹与注入方式，flag 正文不变
- 实现细节：PHP 的 `?>` 会吞掉其后紧跟的一个换行，为保持 base64 独占一行、
  `-->` 独占一行的原版式，echo 末尾显式拼接了 `"\n"`

## 页面行为（均在服务端判断）

| 访问环境 | 表现 |
|---|---|
| iPhone（UA 含 `iPhone`，Safari/微信/QQ 内置浏览器等 iOS 全系） | 200，下发苹果发布会暗色海报风页面：Apple logo + **Only iPhone can do.** + "尊贵的iPhone用户，这份flag为你呈上，点击即可获得" + "马上获得"胶囊按钮，HTML 注释内含动态 flag 的 base64 |
| 其他一切：Android / iPad / Mac / 桌面 / curl / 空 UA | `302 Found` + `Location:` 整蛊视频，**响应体 0 字节，flag 不下发** |

iPad 也被拦（只有 iPhone 才配），呼应梗本身。

flag 以 base64 形式放在 iPhone 分支页面的 HTML 注释里（"求你们不要再嘲笑这些题目了"彩蛋注释下方）。桌面分析者连页面源码都拿不到，只有伪装成 iPhone 才能收到藏 flag 的那份 HTML。

## 出题人配置点（共 2 处）

**1. 整蛊视频地址** — `index.php` 顶部 `$PRANK_URL` 常量。

**2. flag** — 无需改动源码，部署时通过 `FLAG` 环境变量注入（见上节）。
本地想看指定值的效果：

```bash
FLAG="hctf{你的flag}" php -S 127.0.0.1:8080
```

## 部署

生产（Docker，src/ 目录）：

```bash
docker build -t ua_checkin ./src
docker run -d -p 8080:80 -e FLAG="hctf{xxx}" ua_checkin
```

本地快速验证（仓库根目录便携版 PHP 8.5）：

```bash
cd src
../../php/php.exe -S 0.0.0.0:8080        # 或任意 php >= 8
```

黑盒设计：`attachment/` 已移除，选手拿不到源码，预期解法的每一步都只依赖
线上靶机的 HTTP 响应行为（302 目标、`X-Powered-By`、UA 差异化响应），见下节。
`src/` 是唯一源码存放处，仅出题方与部署平台可见。

## 预期解法（签到难度）

1. 电脑/安卓打开 → 被骗视频；iPhone 打开 → 苹果海报页一本正经"尊贵的iPhone用户，这份flag为你呈上"——但页面上没有任何 flag
2. `curl -I` 看到 302 + `X-Powered-By: PHP` → 意识到服务端按 UA 分流
3. `curl -A "<iPhone的UA>" http://xxx/` 伪造 UA 拿到海报页源码 → 注释里 base64 → 解码出 `hctf{...}`
4. 等价路径：DevTools → Network conditions 自定义 UA 刷新后 view-source
5. 考点：UA cloaking 的识别与伪造，curl 自定义 Header，base64

## 测试用 UA

iPhone Safari（iOS 17.5）：

```
Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1
```

注意：iPad UA 是 `iPad`、Mac 是 `Macintosh`，均不含 `iPhone`，都会被 302——这是刻意的。

## 验收

```bash
php -S 127.0.0.1:8089 -t src
python writeup/exp.py http://127.0.0.1:8089     # 输出解码后的 hctf{...}
```

exp.py 为 PoC：伪造 iPhone UA 请求一次，解出注释里的 base64 并打印 flag，
人工与部署时注入的 `$FLAG` 比对即可。拦截分支（非 iPhone UA 一律 302、
响应体 0 字节）按 wp.md 步骤用 `curl -I` 复核。

## 已验证（2026-09-15，PHP 8.5.10 NTS x64）

- curl 默认 UA → 302 整蛊视频，响应体 0 字节
- curl iPhone UA → 200 + 海报页 + 注释 base64，解码 = `hctf{S0urc3_C0d3_D0esnt_L1e}`（回退值）
- `FLAG="hctf{dyn_test}"` 启动 → 同一注释位解码 = `hctf{dyn_test}`（动态注入生效）
- `writeup/exp.py`：17/17 通过；带 `FLAG=hctf{dyn_test}` 运行：18/18 通过（含与环境变量精确比对）
- 与原题 diff：仅注释内 flag 一行不同，其余逻辑与文案逐字节一致

## 已验证（2026-09-16，neko 虚机 Docker + `php:8.3-cli-alpine`）

- Alpine 镜像 157MB（原 `php:8.3-apache` 版 761MB），`php -S` + 8 workers
- 验收版 exp.py（git 历史可溯）曾对线上容器 18/18 通过（含 `FLAG` 环境变量
  精确比对）；后按 PoC 定位改写，对线上容器解出 flag 与注入 `$FLAG` 一致
- Windows 外部访问复核：默认 UA 302 / iPhone UA 200 海报页
