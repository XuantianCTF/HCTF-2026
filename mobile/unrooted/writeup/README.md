# unrooted Writeup

## 1. 静态定位

用 jadx-gui 打开 `unrooted.apk`，包名 `com.example.unrooted`，入口 `MainActivity`：

```kotlin
val status = NativeCheck.checkEnvironment(this)
if (status != 0) {
    result.text = "Environment not clean (0x%x). Refusing to run.".format(status)
    button.isEnabled = false
}
button.setOnClickListener {
    result.text = if (FlagChecker.verify(this, input.text.toString())) {
        "Correct! Welcome to the unrooted side :)"
    } else {
        "Wrong flag, try harder."
    }
}
```

`FlagChecker.verify` 也是先查环境，再调用 native：

```kotlin
fun verify(context: Context, input: String): Boolean {
    if (NativeCheck.checkEnvironment(context) != 0) return false
    return NativeCheck.verifyFlag(input)
}
```

`com.example.unrooted.NativeCheck` 只有两个 `external` 方法，真正逻辑在 `libunrooted.so`：

```kotlin
object NativeCheck {
    init { System.loadLibrary("unrooted") }
    external fun checkEnvironment(context: Context): Int
    external fun verifyFlag(input: String): Boolean
}
```

## 2. 还原 flag

解压 APK，取出 `lib/arm64-v8a/libunrooted.so`（或任意 abi），直接 `strings`：

```bash
unzip -o unrooted.apk 'lib/*' -d out
strings out/lib/arm64-v8a/libunrooted.so | grep -E 'unrooted|PS0m|HCTF'
```

可以看到掩码 `unrooted` 和一段 Base64 密文：

```
PS0mKRQaVTsHXkIbMBpVOxMcQwtbKw8RQBotWwEQF1RECg8=
```

`verifyFlag` 的算法是 `Base64(input XOR "unrooted") == 密文`，反过来解即可：

```python
import base64

secret = "PS0mKRQaVTsHXkIbMBpVOxMcQwtbKw8RQBotWwEQF1RECg8="
mask = b"unrooted"
data = base64.b64decode(secret)
print(bytes(data[i] ^ mask[i % len(mask)] for i in range(len(data))).decode())
# HCTF{n0_r00t_n0_fr1d4_ju5t_4ndr01d}
```

## 3. 分析环境检测

`checkEnvironment` 返回一个位掩码：

| bit | 含义 | 触发条件 |
| --- | --- | --- |
| 0x1 | root | `su` 路径 / Magisk / `ro.build.tags=test-keys` / `ro.debuggable=1` / `ro.secure=0` |
| 0x2 | Frida | `/proc/self/maps`、线程名含 `frida`/`gum-js-loop`/`gmain`，或 27042 端口 |
| 0x4 | 调试器 | `/proc/self/status` 中 `TracerPid > 0` |

root 过的真机、`userdebug` 模拟器通常都会命中 `0x1`，所以直接运行只会看到
`Environment not clean`。

## 4. Frida 绕过

启动一个 `frida-server`（或使用 gadget），spawn 方式注入，确保脚本在 `onCreate`
执行前完成 hook，把 native `checkEnvironment` 的返回值改成 `0`：

```bash
frida -U -f com.example.unrooted -l bypass.js
```

`bypass.js` 通过 `Interceptor.attach` 挂钩 native 导出符号：

```js
const LIB = 'libunrooted.so';
const CHECK = 'Java_com_example_unrooted_NativeCheck_checkEnvironment';
const sym = Module.findExportByName(LIB, CHECK);
Interceptor.attach(sym, { onLeave(retval) { retval.replace(0); } });
```

只绕过环境检测，不改 `verifyFlag`，这样 App 会真正去做 flag 校验。

> 取巧做法：直接 hook Java 层的 `NativeCheck.checkEnvironment` 返回 `0` 同样有效：
> ```js
> Java.perform(() => {
>   Java.use('com.example.unrooted.NativeCheck').checkEnvironment.implementation = () => 0;
> });
> ```

## 5. 验证

输入 `HCTF{n0_r00t_n0_fr1d4_ju5t_4ndr01d}`，点击 `Check`，在绕过检测的前提下会提示
`Correct! Welcome to the unrooted side :)`。

也可以直接跑 `exp.py` 静态还原并确认密文存在于 `libunrooted.so`：

```bash
python3 exp.py ../attachment/unrooted.apk
```
