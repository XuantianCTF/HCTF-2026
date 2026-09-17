# ezgo

出题人：tuxnode

- 方向：Reverse
- 难度：入门 / Easy
- 考点：Golang 逆向、符号表 / 字符串定位、简单异或（XOR）

## 题目描述

一个用 Go 编写的 flag 校验器，输入正确的 flag 才会提示成功。
来试试从 Go 二进制里把隐藏的校验逻辑挖出来吧。

## 题目信息

- 附件：`attachment/ezgo`（选手下载，Go 静态编译的 Linux ELF）
- 远程连接：无（离线题目）
- Flag 格式：`HCTF{...}`
- 二进制信息：

  ```
  Arch:     amd64-64-little
  Type:     statically linked, not stripped
  ```

## 提示

- Go 二进制默认保留符号表，可以先找找 `main.check`
- 字符串 `gopher` 也许不是巧合
- 校验方式很朴素：`输入 ^ key == secret`

## 本地构建与运行

`attachment/` 与 `src/` 下的 Dockerfile 均会编译出题目二进制：

```bash
# 构建并运行
docker build -t rev-ezgo ./attachment
docker run --rm -it rev-ezgo

# 或者直接本地编译
cd attachment && go mod init ezgo && go build -o ezgo . && ./ezgo
```

## 目录结构

```
ezgo/
├── README.md            # 题目说明（本文件）
├── attachment/          # 【公开】给选手的附件与构建 Dockerfile
│   ├── main.go
│   └── Dockerfile
├── src/                 # 【私密】部署用源码与 Dockerfile
│   ├── main.go
│   └── Dockerfile
└── writeup/             # 【私密】解题思路与 exp
    ├── exp.py
    └── README.md
```

## 部署说明

本题为离线逆向题，无需远程服务。`attachment/Dockerfile` 采用多阶段构建，
`builder` 阶段使用 `golang:1.21` 编译出静态 ELF，CI 会从 `/build` 中提取并作为附件发布。
