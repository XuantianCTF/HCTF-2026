# ezjdk Writeup

## 反编译 APK

用 jadx-gui 打开 `ezjdk.apk`，包名 `com.example.myapp`。
从 `MainActivity` 可以看到点击按钮后调用 `FlagChecker.verify`，核心逻辑在 `FlagChecker`：

```kotlin
object FlagChecker {
    private val secret = "LTk+IhASSQYHWwhJNRBbOk4EABlVSw47GVYMWRYYVgc="
    private val mask = "ezjdk"

    fun verify(input: String): Boolean {
        val raw = input.toByteArray(Charsets.UTF_8)
        val enc = ByteArray(raw.size) { i ->
            (raw[i].toInt() xor mask[i % mask.length].code).toByte()
        }
        return Base64.encodeToString(enc, Base64.NO_WRAP) == secret
    }
}
```

## 分析

校验流程为：把输入与 `mask`（`ezjdk`）循环异或，再做 Base64，最后与常量 `secret` 比较。
因此逆向只需两步：先 Base64 解码 `secret`，再与 `mask` 循环异或，即可得到明文 flag。

## 解密

```python
import base64

secret = "LTk+IhASSQYHWwhJNRBbOk4EABlVSw47GVYMWRYYVgc="
mask = b"ezjdk"

data = base64.b64decode(secret)
flag = bytes(data[i] ^ mask[i % len(mask)] for i in range(len(data))).decode()
print(flag)
```

得到：

```
HCTF{w3lc0m3_t0_4ndr01d_r3v3rs3}
```

## 验证

```bash
python3 exp.py
# [+] flag: HCTF{w3lc0m3_t0_4ndr01d_r3v3rs3}
# [+] secret found in ../attachment/ezjdk.apk: True
```

把打印出的 flag 填进 App 的输入框点击 `Check`，会提示
`Correct! You are an Android reverser now :)`。
