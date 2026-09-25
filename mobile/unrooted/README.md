# unrooted

出题人：tuxnode

- 方向：Reverse / Mobile（Android）
- 难度：入门 ~ 中等
- 考点：APK 反编译（jadx）、NDK/so 静态分析、root / Frida / 调试器检测、Frida hook 绕过、异或 + Base64 还原

## 题目描述

这是一款“只在不 root 的环境下才肯工作”的 flag 校验器：启动时会在 native 层检查设备是否 root、是否被调试、是否运行着 Frida。只有环境“干净”时，它才愿意校验你的 flag。

请绕过这些检测，并提交正确的 flag。

## 题目信息

- 附件：`attachment/unrooted.apk`（由 CI 构建发布，Android debug APK）
- 远程连接：无（离线题目）
- Flag 格式：`HCTF{...}`
- App 信息：
  - Package：`com.example.unrooted`
  - minSdk 24 / targetSdk 34
  - 校验入口：`com.example.unrooted.MainActivity` -> `com.example.unrooted.FlagChecker`
  - 关键 native 库：`libunrooted.so`（`com.example.unrooted.NativeCheck`）

## 提示

- Java 层很薄，真正的逻辑在 `libunrooted.so`：
  - `checkEnvironment` 通过 root、Frida、TracerPid 三类检测返回一个状态位掩码；
  - `verifyFlag` 做 `Base64(input XOR "unrooted") == 密文` 的比较。
- 想让它校验，先在 native 层把 `checkEnvironment` 的返回值改成 `0`。
- 密文与掩码都能在 so 里以字符串形式找到。

## 本地构建

`attachment/` 下的 Dockerfile 会在 `builder` 阶段安装 Android SDK + NDK + CMake，编译出 debug APK：

```bash
docker build -t mobile-unrooted --target builder ./attachment
```

构建产物位于镜像的 `/build/unrooted.apk`，可这样取出：

```bash
id=$(docker create mobile-unrooted)
docker cp "$id:/build/unrooted.apk" ./unrooted.apk
docker rm "$id"
```

也可以直接用 Android Studio 打开 `attachment/` 工程构建。

## 目录结构

```
unrooted/
├── README.md            # 题目说明（本文件）
├── attachment/          # 【公开】Android 工程与构建 Dockerfile
│   ├── app/
│   │   └── src/main/
│   │       ├── java/com/example/unrooted/
│   │       └── cpp/                # native root / Frida / debug 检测与校验
│   ├── build.gradle.kts
│   ├── settings.gradle.kts
│   ├── gradle/
│   ├── gradlew
│   └── Dockerfile
└── writeup/             # 【私密】解题思路与 exp
    ├── README.md
    ├── bypass.js
    └── exp.py
```

## 部署说明

本题为离线逆向题，无需远程服务，因此不提供 `src/Dockerfile`。
`attachment/Dockerfile` 采用多阶段构建，`builder` 阶段产出 `/build/unrooted.apk`，
由 CI 提取并以 `unrooted.apk` 作为 Release 附件发布。
