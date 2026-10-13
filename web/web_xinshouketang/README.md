# web_xinshouketang

- **分类**：Web
- **难度**：入门
- **题型**：PPT 课堂 · 新手引导五讲（查看源代码 → HTTP 响应头 → robots.txt → Cookie → POST 请求）
- **附件**：无

## 题面

「CTF 新手课堂」——七页 PPT 式教学站：封面 + 五课 + 结课测试。每课白底极简、
markdown 题面，只讲一个最基础的 Web 功课，讲完直接做课后练习。

- **真 flag 拆分散落**：`FLAG` 环境变量内容恰好 5 段下划线分隔，容器启动时拆成
  五块，分别藏在与当课知识点对应的真实位置（源码注释 / 响应头 / robots.txt
  引出的路径 / Cookie / POST 接口），课后练习题面只说做练习、不提碎片
- **题内零校验**：结课测试页只做客户端拼接（五个文本框按课号标注，自动带上
  flag 头 + 复制按钮），对错与提示全部由平台 checker 返回
- **打卡蜜罐（anti-agent）**：每课「我已学会」按钮发**假碎片**（静态随机 hex，
  与真碎片同量级、肉眼不可分辨），第 5 次打卡还怂恿拼起来提交；集齐拼出的
  假 flag 交给平台会被逐块回怼「老实学「知识点名」，很无趣吧」

## 提示

1. 第一课的碎片在「查看源代码」才能看到的地方，页面上是找不到的
2. 第三课先把 `/robots.txt` 每一行读完，特别是被「禁止访问」的那行
3. 结课测试五个框对应五课的课后练习——打卡奖励和课后练习不是一回事

## 部署

```bash
docker build -t xinshouketang ./src
docker run -d -p 58000:80 -e FLAG="HCTF{a_b_c_d_e}" xinshouketang
```

- 服务监听容器内 `0.0.0.0:80`（`python:3.12-alpine` + FastAPI/uvicorn，
  纯 Python 单容器，无 nginx、无数据库、无 CDN）
- **动态 flag**：平台向容器注入 `FLAG` 环境变量；**内容必须恰好 5 段下划线
  分隔**（启动即校验，段数不对拒绝起服务），按 `_` 拆成五块散落各课；
  未注入时回退 `HCTF{we1c0me_t0_web_ctf_2026}`
- **平台 checker**（ret2shell，随题配置、不进本仓库）：dynamic-leet 模板，
  `PREFIX = "HCTF"`，`TEMPLATE = "welcome_to_web_ctf_class"`（4 个下划线 = 5 块，
  leet 隐写只替换字母数字、下划线保留，队标 id 十六进制尾巴追加在最后一块
  末尾，因此按 `_` 拆恒为 5 段）；错误提交用 `regex::test` 逐块识别假碎片并
  返回「老实学……，很无趣吧」，五块全假再加一句点破，其余 Incorrect + 换队审计

## 碎片藏点速查（出题人向）

| 课 | 考点 | 碎片（= FLAG 第 N 段）藏在 | 练习动作 |
|---|---|---|---|
| 1 查看源代码 | Ctrl+U / HTML 注释 / F12 | `/lesson/1` 源码内 HTML 注释 `第 1 块：...` | 看本页源代码 |
| 2 HTTP 响应头 | F12 Network / `curl -D -` | `/lesson/2` 响应头 `X-Hint: piece-2: ...` | 抄下自定义字段 |
| 3 robots.txt | robots 协议 / Disallow 泄露 | `/robots.txt` → `Disallow: /hidden-notes/` → 教师备忘页 | 勿入被禁路径 |
| 4 Cookie | Application 面板 / Set-Cookie | `/lesson/4` 下发 `Set-Cookie: xiaozhitiao=<piece4>`（`visitor=guest` 陪衬） | 拆小纸条 |
| 5 POST 请求 | `curl -X POST` / fetch | `POST /api/lesson5`（GET 返回 405 教学提示） | 用 POST 访问接口 |

打卡假碎片（`/api/learn/{n}` 返回，静态）：

| 课 | 假碎片 | checker 回怼 |
|---|---|---|
| 1 | `src-4c8e` | 老实学「查看源代码」，很无趣吧 |
| 2 | `hdr-b3d7` | 老实学「HTTP 响应头」，很无趣吧 |
| 3 | `rbt-e9a1` | 老实学「robots.txt」，很无趣吧 |
| 4 | `ck-62f4` | 老实学「Cookie」，很无趣吧 |
| 5 | `post-ad05` | 老实学「POST 请求」，很无趣吧 |

改动假碎片值时，checker 内 5 个 `regex::test` 模式必须同步修改。
