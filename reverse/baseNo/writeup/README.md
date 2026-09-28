# baseNo Writeup

## 1. 定位校验逻辑

本题为未 strip 的 C 程序，直接丢进 IDA / Ghidra，或先用 `strings` 找线索：

```bash
strings attachment/baseNo | grep -iE 'HCTF|Correct|Wrong|input'
strings attachment/baseNo | grep -E '^[A-Za-z0-9+/=]{40,}$'
```

能看到：

- 第二行会命中一个 64 字节的神秘字符串（就是自定义密码表）；
- `main` 里调用了 `check`，失败输出 `Wrong!`，成功输出 `Correct!`。

```c
static const char *TABLE =
    "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm0123456789+/";

static const unsigned char KEY[4] = {'H', 'C', 'T', 'F'};

static const unsigned char CIPHER[] = {
    0x04, 0x17, 0x12, 0x1e, 0x03, 0x25, 0x2e, 0x36, 0x3a, 0x19, 0x17, 0x76,
    0x0c, 0x16, 0x65, 0x3f, 0x06, 0x33, 0x1f, 0x2b, 0x0c, 0x72, 0x6c, 0x74,
    0x0e, 0x1a, 0x6c, 0x75, 0x0e, 0x16, 0x04, 0x2a, 0x0c, 0x70, 0x64, 0x7b,
};
```

## 2. 分析 check

`check` 做的是标准的“编码后比对”，一共两层变换：

```c
static int check(const char *flag)
{
    char enc[512];
    size_t n = custom_b64((const unsigned char *)flag, strlen(flag), enc);

    if (n != sizeof(CIPHER))          // 密文长度 = base64 输出长度
        return 0;

    for (size_t i = 0; i < n; i++) {
        if ((unsigned char)(enc[i] ^ KEY[i % 4]) != CIPHER[i])
            return 0;
    }
    return 1;
}
```

1. `custom_b64`：和标准 base64 完全一样，只是把索引字母表换成了 `TABLE`（A-Z 被 `qwerty...` 打乱）；
2. 再对编码结果逐字节异或 `KEY = "HCTF"`（4 字节循环）。

## 3. 解密

加密是对称的，反向操作即可：

1. `CIPHER[i] ^ KEY[i % 4]` 得到自定义表下的 base64 文本；
2. 把自定义表映射回标准表 `A-Za-z0-9+/`，直接 `base64.b64decode`。

```python
TABLE = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm0123456789+/"
STD   = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
KEY   = b"HCTF"

encoded = bytes(c ^ KEY[i % 4] for i, c in enumerate(CIPHER)).decode()
flag    = base64.b64decode(encoded.translate(str.maketrans(TABLE, STD))).decode()
print(flag)
```

得到：

```
HCTF{cu5t0m_b4s3_64_74bl3}
```

## 4. 验证

```bash
python3 exp.py                 # 自动读取 ../attachment/baseNo 验证
# 或手动
echo 'HCTF{cu5t0m_b4s3_64_74bl3}' | ./attachment/baseNo
# Correct! You cracked the custom table :)
```

## 考点小结

- 字符串定位 / 识别自定义字母表；
- 认清“自定义 base64”只是换了 table，结构不变；
- 逆向中逐层剥离组合变换（自定义编码 + 异或）。
