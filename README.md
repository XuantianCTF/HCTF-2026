# HCTF 2026

本仓库作为HCTF-2026的题目规范化存储，保证题目可回溯，可复现

## 目录结构

```
ctf-challenges/
├── .github/                     # GitHub Actions 自动化部署配置
│   └── workflows/
│       ├── deploy.yml           # 自动构建并部署到解题平台/服务器
├── README.md                    # 仓库说明、分类索引
├── web/                         # 题目分类：Web
│   ├── web_ez_sqli/             # 每一个具体题目作为一个文件夹
│   └── web_phar_serialize/
│
├── pwn/                         # 题目分类：Pwn
│   └── pwn_stack_overflow/
│
├── crypto/                      # 题目分类：密码学
│   └── crypto_rsa_variant/
│
├── reverse/                     # 题目分类：逆向
│   └── ezgo/
│
└── misc/                        # 题目分类：杂项
    └── misc_forensics/
```

## 单题目录结构

以 `web/web_ez_sqli/` 为例，每个题目统一采用如下结构：

```
web_ez_sqli/
├── README.md                    # 题目说明
├── attachment/                  # 【公开】给选手下载的附件
│   ├── app.py                   # 过滤后的源码/编译后的二进制
│   └── Dockerfile               # 允许选手本地搭建环境的 Dockerfile（脱敏）
│
├── src/                         # 【私密/内部】题目原始代码与构建依赖
│   ├── html/
│   │   └── index.php
│   └── Dockerfile               # 实际用于部署生产环境的 Dockerfile
│
├── writeup/                     # 【私密】解题思路与 Payload
│   ├── exp.py                   # 自动化验证脚本 (PoC/Exp)
│   └── README.md                # 详细解题步骤
│
└── config/                      # 题目特定配置文件（如数据库初始化）
    └── init.sql
```

## 题目提交指南

先`fork`本仓库，并clone自己fork后的仓库

并在当前最新的main分支下执行

```bash
git checkout -b "题目名称"  # 在最新main分支的基础上创建分支
```

随后向本仓库提交[Pull Request](https://docs.github.com/en/pull-requests/reference/pull-requests)


## 镜像构建说明

### 版本

题目与底层的libc无关时，建议使用alpine版本的镜像作为运行时环境

### 动态flag

本次采用[ret2shell](https://github.com/ret2shell/ret2shell)平台，

**容器动态flag会自动输出到`FLAG`环境变量中**

所以在出题时请注意，或在**ret2shell**平台进行特殊配置

### attachment/Dockerfile 编写规范

`attachment/` 是【公开】给选手的附件目录，其中的 `Dockerfile` 既用于选手本地复现，也被 CI 用于自动构建并发布附件二进制。

编写要求：

1. **必须使用多阶段构建，且编译阶段命名为 `builder`**。CI 会执行 `docker build --target builder`：

   ```dockerfile
   FROM ubuntu:22.04 AS builder
   WORKDIR /build
   COPY vuln.c .
   RUN gcc vuln.c -o vuln -fno-stack-protector -no-pie
   ```

2. **编译产物必须输出到 `/build` 目录**。CI 会从该阶段容器的 `/build` 中提取 ELF 可执行文件并重命名为题目名，作为 Release 附件发布；若未找到 ELF 二进制，构建直接失败。

3. **如需附带动态链接器与 libc**（pwn 题常需要），在 `builder` 阶段把它们拷到 `/build/libc/`：

   ```dockerfile
   RUN mkdir -p /build/libc \
       && cp /lib/x86_64-linux-gnu/libc.so.6 /build/libc/ \
       && cp -L /lib64/ld-linux-x86-64.so.2 /build/libc/
   ```

   CI 检测到 `/build/libc/` 非空时，会把二进制与这些文件一起打包为 `<题目名>.zip` 发布；否则只发布原始二进制文件。libc 版本由基础镜像决定，作者可自行选择/固定。

4. **运行阶段负责本地复现**，通过固定端口暴露服务（如用 `socat`）：

   ```dockerfile
   FROM ubuntu:22.04
   RUN apt-get update \
       && apt-get install -y --no-install-recommends socat \
       && rm -rf /var/lib/apt/lists/*
   WORKDIR /app
   COPY --from=builder /build/vuln /app/vuln
   EXPOSE 9999
   CMD ["socat", "TCP-LISTEN:9999,reuseaddr,fork", "EXEC:/app/vuln"]
   ```

5. **统一使用 Linux/amd64 + glibc 基础镜像编译**（如 `ubuntu:22.04`），不要依赖宿主机工具链，避免本地（macOS/ARM）与线上架构不一致。

6. **只放演示 flag**，不要写入真实 flag；附件会被公开发布。动态 flag 由部署镜像（`src/`）从 `FLAG` 环境变量读取。

7. **附件镜像不推送到 ghcr**。CI 仅在 PR 校验与发布时构建/提取产物；需要发布部署镜像时请编写 `src/Dockerfile`。


### 逆向场景

如果不需要构建在线平台镜像,就不要在`src/`目录下写Dockerfile

只在attachment目录下写Dockerfile即可,该目录下的Dockerfile编写规则同上
