# web_ua_checkin

- **分类**：Web / 黑盒（无附件，仅线上靶机）
- **难度**：签到
- **题型**：HTTP 头认知与伪造（UA cloaking）+ 编码还原

## 题面

"这份资料，为 iPhone 独占打造。"

一个一本正经宣称 **Only iPhone can do.** 的页面：用 iPhone 打开是苹果
发布会暗色海报风的自证页面；用其他任何设备（Android、iPad、桌面浏览器、
curl……）打开，都会被 302 送去一个不相干的视频。

flag 藏在某个分支的响应里——前提是你得先收到那份响应。

## 部署

```bash
docker build -t ua_checkin ./src
docker run -d -p 8080:80 -e FLAG="hctf{xxx}" ua_checkin
```

- 单文件 PHP 页面，`php:8.3-cli-alpine` + PHP 内置服务器（`php -S`），容器内监听 80 端口，无外部依赖
- 纯 PHP 脚本与底层 libc 无关，按仓库规范使用 alpine 底座
- **动态 flag**：平台向容器注入 `FLAG` 环境变量；未注入时使用代码内回退值

## 说明

详细解题思路与验收脚本见 `writeup/`（仅供出题方与评委）。
