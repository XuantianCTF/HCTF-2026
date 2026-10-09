# signin

出题人：tuxnode

- 方向：Reverse
- 难度：签到 / Warmup
- 考点：PE 逆向、数据定位、字符数组还原

## 题目描述

欢迎来到 HCTF 2026 逆向方向！这是一道签到题。
程序内部藏着一个字符数组，输入正确的 flag 才能通过校验。
把它找出来提交即可。

## 题目信息

- 附件：`attachment/signin.exe`（选手下载，Windows PE，未 strip）
- 远程连接：无（离线题目）
- Flag 格式：`HCTF{...}`
- 二进制信息：

  ```
  Arch:     x86-64
  Type:     PE32+ executable (console), statically linked, not stripped
  ```

## 提示

- 先随便输入试试，失败会提示 `Wrong!`
- 静态分析：找 `main`，看那个 `enc` 数组
- 数组里的值都是可打印字符，按顺序还原就是 flag

## 本地构建与运行

`attachment/` 下的 Dockerfile 会编译出题目二进制（`builder` 阶段，CI 从 `/build` 提取 PE 并重命名为 `signin.exe`）：

```bash
# 构建并运行
docker build -t rev-signin ./attachment
docker run --rm -it rev-signin

# 或者直接本地交叉编译（Windows PE）
cd attachment && x86_64-w64-mingw32-gcc -O2 -static -o signin.exe signin.c

# 本地有 wine 的话可以直接跑
# wine signin.exe
```

## 目录结构

```
signin/
├── README.md            # 题目说明（本文件）
├── attachment/          # 【公开】给选手的附件与构建 Dockerfile
│   ├── signin.c
│   └── Dockerfile
└── writeup/             # 【私密】解题思路与 exp
    ├── exp.py
    └── README.md
```

## 部署说明

本题为离线逆向题，无需远程服务，也不需要在 `src/` 下写 Dockerfile。
`attachment/Dockerfile` 采用多阶段构建，`builder` 阶段使用
`gcc-mingw-w64-x86-64` 在 Linux/amd64 下交叉编译出 Windows PE，
CI 会从 `/build` 中提取并作为 `signin.exe` 发布。
