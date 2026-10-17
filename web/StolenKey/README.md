# StolenKey

- **分类**：Web
- **难度**：困难
- **题型**：SSH 弱口令 + `/etc/skel` 属主配置错误 + cron 定时任务提权
- **附件**：无

## 题面

一台对外只开放 SSH 的跳板机，低权限账号 `guest` 的密码就写在登录提示里。
管理员账号每分钟都会被系统重建一次，flag 藏在他的家目录中。

目标：读取 `/root/flag.txt`。

## 提示

1. `guest / guest` 登录后，看看谁拥有 `/etc/skel`。
2. 定时任务会以 root 身份重建 `admin`，并把 flag 放进 `admin` 的家目录。
3. 新用户的家目录来自 `/etc/skel`，而 `admin` 登录时会执行其中的 `.bashrc`。

## 部署

```bash
docker build -t stolenkey ./src
docker run -d -p 58022:22 -e FLAG="HCTF{xxx}" stolenkey
ssh guest@127.0.0.1 -p 58022
```

- 服务监听容器内 `0.0.0.0:22`，宿主端口示例为 `58022`
- **动态 flag**：平台通过 `FLAG` 环境变量注入，容器启动时写入 `/root/flag.txt`
  （权限 `600`）；未注入时使用代码内的本地演示值
- 定时任务每分钟执行一次，漏洞点在 `/etc/skel` 的属主设置
