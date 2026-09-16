# web_kan_yi_dao

- **分类**：Web
- **难度**：简单
- **题型**：剧情向电商砍价页渗透（接口发现 + 水平越权 IDOR）
- **附件**：无

## 题面

「砍价免费拿」：孤品 flag 一件，标价 199 元，当前已砍至 0.0120 元，
再砍几刀即可 0 元包邮到家。页面复刻拼夕夕式砍价全体验——金币/金粒/碎片
单位换算链、幸运大转盘、红包雨、好友助力、三层挽留弹窗、倒计时清零威胁。


## 部署

```bash
python writeup/tools/build_frontend.py   # 从 index.dev.html 构建混淆前端（源码仓库内执行）
docker build -t kan_yi_dao ./src
docker run -d -p 8931:8931 -e FLAG="hctf{xxx}" kan_yi_dao
```

- 服务监听容器内 `0.0.0.0:8931`，纯 Python 3 标准库实现，无外部依赖
- **动态 flag**：平台向容器注入 `FLAG` 环境变量；未注入时使用代码内回退值（保持 `hctf{}` 格式）
- 本题含一个静态诱饵 flag（与真 flag 同为 `hctf{}` 前缀、值不同，判分对比注入值时应判错），详见 `writeup/`

