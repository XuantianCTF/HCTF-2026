# overflow

出题人：tux

- 方向：Pwn
- 难度：入门 / Easy
- 考点：栈溢出、ret2win

## 题目描述

你的消息好像有点太长了……

## 题目信息

- 附件：`attachment/vuln`（选手下载）
- 远程连接：`nc <host> <port>`
- Flag 格式：`flag{...}`
- 二进制保护：

  ```
  Arch:     amd64-64-little
  RELRO:    Partial RELRO
  Stack:    No canary found
  NX:       NX disabled
  PIE:      No PIE
  ```

## 提示

- `gets` 没有长度检查
- 程序里有一个你从没见过的函数

## 本地构建与运行

`attachment/` 与 `src/` 下的 Dockerfile 均会自动编译题目二进制并启动服务：

```bash
# 部署版本（动态 flag 从环境变量 FLAG 读取）
docker build -t pwn-overflow ./src
docker run --rm -p 9999:9999 -e FLAG='flag{test_flag}' pwn-overflow

# 本地测试（固定 demo flag）
docker build -t pwn-overflow-demo ./attachment
docker run --rm -p 9999:9999 pwn-overflow-demo

# 连接
nc 127.0.0.1 9999
```

## 目录结构

```
overflow/
├── README.md            # 题目说明（本文件）
├── attachment/          # 【公开】给选手的附件与本地复现 Dockerfile
│   ├── vuln.c
│   ├── Dockerfile
│   └── flag.txt
├── src/                 # 【私密】部署用源码与 Dockerfile
│   ├── vuln.c
│   ├── entrypoint.sh
│   └── Dockerfile
└── writeup/             # 【私密】解题思路与 exp
    ├── exp.py
    └── README.md
```

## 部署说明

`src/Dockerfile` 采用多阶段构建：第一阶段使用 `gcc` 编译二进制，第二阶段仅保留 `socat` 与二进制运行。

容器启动时 `entrypoint.sh` 会将环境变量 `FLAG` 写入 `/flag`（ret2shell 平台会自动注入动态 flag），再通过 `socat` 在 `9999` 端口监听。
