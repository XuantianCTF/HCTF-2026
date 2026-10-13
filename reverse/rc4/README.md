# rc4

出题人：tuxnode

- 方向：Reverse
- 难度：简单 / Easy
- 考点：标准 RC4、静态分析、流密码解密

## 题目描述

程序会用 RC4 加密输入并与内置密文比较。找到密钥和密文，按照程序使用的标准 RC4 算法还原 flag。

## 题目信息

- 附件：`rc4.exe`（选手下载，Windows x86-64 PE）
- 远程连接：无（离线题目）
- Flag 格式：`HCTF{...}`
- 运行方式：Windows；Linux / macOS 下可使用 Wine

## 提示

- 找到密钥和待比较的密文。
- 确认 KSA 初始化 256 字节状态，并留意 PRGA 的状态更新顺序。
- RC4 是对称流密码：用同一密钥对密文再异或一次即可还原明文。

## 本地构建与运行

`attachment/` 下的 Dockerfile 会在 `builder` 阶段交叉编译 Windows PE。CI 从 `/build` 提取 `.exe` 并作为附件发布。

```bash
docker build -t rev-rc4 ./attachment
docker run --rm -i rev-rc4
# Input flag: HCTF{...}
```

也可以直接在 Windows 上运行下载的 `rc4.exe`，或在 Linux / macOS 上使用 Wine：

```bash
wine rc4.exe
```

## 目录结构

```text
rc4/
├── README.md
├── attachment/
│   ├── Dockerfile
│   └── rc4.c
└── writeup/
    ├── README.md
    └── exp.py
```

## 部署说明

本题为离线逆向题，无需远程服务，也无需 `src/Dockerfile`。附件镜像使用 MinGW-w64 在 Linux/amd64 下交叉编译 x86-64 Windows PE，`builder` 阶段生成的可执行文件位于 `/build/rc4.exe`，符合仓库附件 CI 的 PE 提取规则；镜像运行阶段通过 Wine 启动该程序，便于本地验证。
