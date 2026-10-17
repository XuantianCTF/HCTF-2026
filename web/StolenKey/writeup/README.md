# StolenKey Writeup

## 漏洞点

1. 镜像把整个 `/etc/skel` 目录 `chown` 给了 `guest`，普通用户可以任意修改
   新用户家目录的模板文件。
2. `/etc/cron.d/admin-job` 每分钟以 root 身份执行一次：
   - 删除并重建 `admin` 用户（`useradd -m` 会复制 `/etc/skel`）；
   - 把 `/root/flag.txt` 复制为 `/home/admin/.flag`（权限 `400`，属主 admin）；
   - 以 `su -l admin -c 'bash --login -i -c exit'` 启动登录 shell。
3. `admin` 的交互式登录 shell 会加载 `~/.bashrc`。因此 `guest` 往
   `/etc/skel/.bashrc` 追加的命令，会在一分钟后的 cron 任务中以 `admin`
   身份执行，从而读到 `.flag`。

## 利用思路

`guest / guest` SSH 登录后，向 `/etc/skel/.bashrc` 追加：

```bash
echo 'cp ~/.flag /tmp/flag && chmod 644 /tmp/flag' >> /etc/skel/.bashrc
```

等待下一次 cron 触发。`admin` 的登录 shell 执行上述命令，将 flag 复制到
所有人可读的 `/tmp/flag`，随后直接读取即可：

```bash
cat /tmp/flag
```

## exp

```bash
./exp.sh HOST 58022
```

脚本会自动向 `/etc/skel/.bashrc` 写入 payload，并轮询 `/tmp/flag`。
安装了 `sshpass` 时会自动使用 `guest` 密码；否则交互式输入一次密码即可
（脚本使用 SSH ControlMaster 复用连接）。

## 修复建议

- 不要让低权限用户拥有 `/etc/skel` 或其中的模板文件。
- 定时任务创建账号时使用可信目录，避免从用户可写的模板派生家目录。
- 不要在以 root 身份运行的账号重建流程中自动执行登录 shell 配置。
