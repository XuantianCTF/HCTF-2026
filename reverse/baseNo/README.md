# baseNo

出题人：tuxnode

- 方向：Reverse
- 难度：入门 / Easy
- 考点：C 逆向、字符串定位、自定义编码表（custom base64 alphabet）、异或

## 题目描述

程序用一张“被打乱过的 base64 密码表”校验 flag，密文里还压了一层异或。
找出那张表，把两层都剥掉，就能拿到 flag。

## 题目信息

- 附件：`attachment/baseNo`（选手下载，Linux ELF，未 strip）
- 远程连接：无（离线题目）
- Flag 格式：`HCTF{...}`
- 二进制信息：

  ```
  Arch:     amd64-64-little
  Type:     dynamically linked, not stripped
  ```

## 提示

- 先用 `strings` 找找那张表
- `check` 里有两步：先查表编码，再逐字节异或
- 异或的密钥长得像比赛的缩写

## 本地构建与运行

`attachment/` 下的 Dockerfile 会编译出题目二进制（`builder` 阶段，CI 从 `/build` 提取 ELF）：

```bash
# 构建并运行
docker build -t rev-baseno ./attachment
docker run --rm -it rev-baseno

# 或者直接本地编译
cd attachment && gcc -O2 -o baseNo baseNo.c && ./baseNo
```

## 目录结构

```
baseNo/
├── README.md            # 题目说明（本文件）
├── attachment/          # 【公开】给选手的附件与构建 Dockerfile
│   ├── baseNo.c
│   └── Dockerfile
├── src/                 # 【私密】部署用源码
│   └── baseNo.c
└── writeup/             # 【私密】解题思路与 exp
    ├── exp.py
    └── README.md
```

## 部署说明

本题为离线逆向题，无需远程服务，也不需要在 `src/` 下写 Dockerfile。
`attachment/Dockerfile` 采用多阶段构建，`builder` 阶段使用 `gcc:13-bookworm`
在 Linux/amd64 下编译出 ELF，CI 会从 `/build` 中提取并作为附件发布。
