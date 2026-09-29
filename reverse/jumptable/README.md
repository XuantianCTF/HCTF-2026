# jumptable

出题人：tuxnode

- 方向：Reverse
- 难度：入门 / Easy
- 考点：汇编逆向、`jmp rax` 跳转表、手工构造的 256 项查表、Linux syscall

## 题目描述

一道用纯汇编（`.intel_syntax`）手写的 flag 读取器。程序把你的第一个参数按字节查表后
`jmp rax`，只有落进 `success` 分支才会用 `open/read/write` 把 `/flag` 的内容打出来。
跳转表被塞在代码段里，`objdump` 会把它当成一堆莫名其妙的指令。

线上环境提供 SSH，预装了 `gdb`、`objdump`、`strace` 等工具，可以直接动态调试试出来。
（`/flag` 只有 root 可读，而 `checker` 是 setuid root，所以必须通过程序读 flag。）

## 题目信息

- 附件：`attachment/checker.S`（选手下载，纯汇编源码；CI 会编译出 Linux ELF 附件）
- 远程连接：SSH，用户名 `ctf`，密码 `ctf`，端口 `22`
- Flag 格式：`HCTF{...}`（由部署容器从 `FLAG` 环境变量写入 `/flag`）
- 二进制信息：

  ```
  Arch:     amd64-64-little
  Type:     statically linked, not stripped
  ```

## 提示

- `_start` 里取的是 `[rsp+16]`，也就是 `argv[1]`，只看了它的第一个字节
- 表在 `.text` 里，`objdump -d` 反出来的“指令”其实是一串 8 字节地址
- `gdb` 里在 `jmp rax` 之前看一眼 `rax` 就够了

## 本地构建与运行

`attachment/` 下的 Dockerfile 会编译出题目二进制（`builder` 阶段，CI 从 `/build` 提取 ELF）：

```bash
# 构建
docker build -t rev-jumptable ./attachment

# 需要先准备一个 /flag（读取的是容器内的绝对路径 /flag）
printf 'HCTF{local_test_flag}\n' > flag
docker run --rm -v "$PWD/flag:/flag:ro" rev-jumptable k_anything

# 也可以本地直接编译
cd attachment && as --64 -o checker.o checker.S && ld -o checker checker.o -z noexecstack && ./checker k
```

## 目录结构

```
jumptable/
├── README.md            # 题目说明（本文件）
├── attachment/          # 【公开】给选手的附件与构建 Dockerfile
│   ├── checker.S
│   └── Dockerfile
├── src/                 # 【私密】SSH 线上环境源码与 Dockerfile
│   ├── checker.S
│   ├── entrypoint.sh
│   └── Dockerfile
└── writeup/             # 【私密】解题思路与 exp
    ├── exp.py
    └── README.md
```

## 部署说明

`src/Dockerfile` 用于部署在线环境：

- `builder` 阶段用 `as` + `ld` 编译静态 ELF；
- 运行阶段安装 `openssh-server`、`gdb`、`binutils`、`strace`、`ltrace` 等工具；
- 启动时 `entrypoint.sh` 把动态 flag 写入 `/flag`（`root:root 0400`），
  并把 `checker` 设为 setuid root（`4755`），玩家必须以程序读取 flag；
- `EXPOSE 22`，通过 SSH 登录（`ctf` / `ctf`）。

`attachment/Dockerfile` 只负责编译并发布附件二进制，不参与线上部署。
