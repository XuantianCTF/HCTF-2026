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
