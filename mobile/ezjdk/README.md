# ezjdk

出题人：tuxnode

- 方向：Reverse / Mobile（Android）
- 难度：入门 / Easy
- 考点：APK 反编译（jadx）、Java/Kotlin 层静态校验、Base64 + 异或还原

## 题目描述

一个写着 “flag 校验器” 的安卓小应用：输入正确的 flag 才会提示成功。
APK 没有加壳也没有混淆，拿好你的 jadx，开始第一次安卓逆向吧。

## 题目信息

- 附件：`attachment/ezjdk.apk`（由 CI 构建发布，Android debug APK）
- 远程连接：无（离线题目）
- Flag 格式：`HCTF{...}`
- App 信息：
  - Package：`com.example.myapp`
  - minSdk 24 / targetSdk 34
  - 校验入口：`com.example.myapp.MainActivity` -> `com.example.myapp.FlagChecker`

## 提示

- 直接用 jadx-gui 打开 APK，从 `MainActivity` 跟到校验函数
- 密文是一段 Base64，旁边还有一个字符串常量，多半就是 key
- 校验方式很朴素：`Base64(input XOR key) == secret`

## 本地构建

`attachment/` 下的 Dockerfile 会在 `builder` 阶段用 Android SDK 编译出 debug APK：

```bash
docker build -t mobile-ezjdk --target builder ./attachment
```

构建产物位于镜像的 `/build/ezjdk.apk`，可这样取出：

```bash
id=$(docker create mobile-ezjdk)
docker cp "$id:/build/ezjdk.apk" ./ezjdk.apk
docker rm "$id"
```

也可以直接用 Android Studio 打开 `attachment/` 工程构建。

## 目录结构

```
ezjdk/
├── README.md            # 题目说明（本文件）
├── attachment/          # 【公开】Android 工程与构建 Dockerfile
│   ├── app/
│   ├── build.gradle.kts
│   ├── settings.gradle.kts
│   ├── gradle/
│   ├── gradlew
│   └── Dockerfile
└── writeup/             # 【私密】解题思路与 exp
    ├── exp.py
    └── README.md
```

## 部署说明

本题为离线逆向题，无需远程服务，因此不提供 `src/Dockerfile`。
`attachment/Dockerfile` 采用多阶段构建，`builder` 阶段产出 `/build/ezjdk.apk`，
由 CI 提取并以 `ezjdk.apk` 作为 Release 附件发布。
