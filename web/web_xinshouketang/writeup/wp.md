# web_xinshouketang 通关记（wp）

## 踩坑起步：打卡奖励不是碎片

进站是七页 PPT 式课堂，每课下方一个「我已学会」按钮。我图快，五课全部点完，
打卡奖励拿到五串：`src-4c8e`、`hdr-b3d7`、`rbt-e9a1`、`ck-62f4`、`post-ad05`。
到结课测试填进五个框，拼出：

```
HCTF{src-4c8e_hdr-b3d7_rbt-e9a1_ck-62f4_post-ad05}
```

交平台，五连暴击：

```
第 1 块是打卡奖励：老实学「查看源代码」，很无趣吧
第 2 块是打卡奖励：老实学「HTTP 响应头」，很无趣吧
第 3 块是打卡奖励：老实学「robots.txt」，很无趣吧
第 4 块是打卡奖励：老实学「Cookie」，很无趣吧
第 5 块是打卡奖励：老实学「POST 请求」，很无趣吧
```

外加一句「按钮按得挺勤，课是一节都没上啊」。行，老实上课。课后练习才是
碎片的出处——每课练的就是当堂讲的那个知识，碎片就藏在用得上这个知识的地方。

## 第一课 · 查看源代码

题面说网页看到的是「装修完」的样子，源代码才是原始交付。在 `/lesson/1`
按 `Ctrl + U`，页面底部一段 HTML 注释：

```
<!--
  第 1 块：we1c0me
  能在源代码里看到这行注释，第一课就算学会了
-->
```

浏览器不渲染注释，但 `view-source` 一直都在。拿到第 1 块。

## 第二课 · HTTP 响应头

响应头是服务器先递过来的「看不见的清单」。`curl -s -D - -o /dev/null`（注意
`curl -I` 发的是 HEAD，这个站只回 GET）看 `/lesson/2` 的响应头：

```
x-hint: piece-2: t0
```

F12 → Network → 点第一个请求 → Response Headers 也能看到同一行。第 2 块：`t0`。

## 第三课 · robots.txt

网址后面加 `/robots.txt`：

```
User-agent: *
Disallow: /api/
Disallow: /hidden-notes/
```

「请勿入内」就是「快来」。访问 `/hidden-notes/`，教师备忘页大大方方写着
「第 3 块」，还夸了句会翻游客须知的学生前途无量。

## 第四课 · Cookie

打开 `/lesson/4` 时服务器塞了两个 Cookie（F12 → Application → Cookie）：
`visitor=guest` 是陪衬，`xiaozhitiao=<第 4 块>` 才是那张小纸条。

## 第五课 · POST 请求

`/api/lesson5` 用 GET 敲门只回 405，还贴心提示「GET 是我要看，POST 是我要交」：

```bash
curl -X POST http://HOST:58000/api/lesson5
# {"msg":"第五课通过，POST 用得很熟练，这串拿好。","flag_part":"2026"}
```

第 5 块到手。

## 结课测试

五个框按课号填好，点「拼出 flag」，前端自动拼成
`HCTF{we1c0me_t0_web_ctf_2026}`，复制交平台：Correct。

## 复盘

- 打卡按钮是蜜罐：奖励碎片与真碎片同量级随机 hex，不看内容只看长相分不出来
- checker 的嘲讽就是索引——它点名哪课，就回哪课做练习
- 真碎片来自 `FLAG` 环境变量拆分（leet 隐写按队不同，照抄别人的会命中换队审计）
