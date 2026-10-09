# signin Writeup

## 1. 试跑与定位

签到题先跑一下（附件是 Windows PE，Linux 下用 wine 运行）：

```bash
wine attachment/signin.exe
# ==========================================
#             HCTF 2026 | Sign-in
# ==========================================
# Please input the flag: test
# Wrong! Keep trying :(
```

失败提示 `Wrong!`，说明程序在比较某个内嵌常量。

## 2. 静态分析

丢进 IDA / Ghidra，定位 `main`，会看到校验逻辑：

```c
static const int enc[] = {
    'H', 'C', 'T', 'F', '{', 'w', '3', 'l', 'c', '0', 'm', '3', '_', '7',
    '0', '_', 'H', 'C', 'T', 'F', '_', '2', '0', '2', '6', '}',
};

int main(void)
{
    const unsigned n = sizeof(enc) / sizeof(enc[0]);
    char buf[128];

    printf("Please input the flag: ");
    fgets(buf, sizeof(buf), stdin);
    buf[strcspn(buf, "\r\n")] = '\0';

    if (strlen(buf) != n) {
        printf("Wrong! Keep trying :(\n");
        return 0;
    }

    for (unsigned i = 0; i < n; i++) {
        if ((unsigned char)buf[i] != (char)enc[i]) {
            printf("Wrong! Keep trying :(\n");
            return 0;
        }
    }

    printf("Correct! Welcome to HCTF 2026 :)\n");
    return 0;
}
```

`enc` 里每个元素都是一个可打印字符的 ASCII 码，按顺序拼起来即是 flag。
`objdump -s -j .rdata` 也能直接看到这段数据：

```
H C T F { w 3 l c 0 m 3 _ 7 0 _ H C T F _ 2 0 2 6 }
```

## 3. 解密

```python
enc = [ord(c) for c in "HCTF{w3lc0m3_70_HCTF_2026}"]
print("".join(chr(c) for c in enc))
```

得到：

```
HCTF{w3lc0m3_70_HCTF_2026}
```

## 4. 验证

```bash
python3 exp.py                 # 自动读取并把 flag 作为输入提交给 ../attachment/signin.exe
# 或手动
echo 'HCTF{w3lc0m3_70_HCTF_2026}' | wine attachment/signin.exe
# Correct! Welcome to HCTF 2026 :)
```

## 考点小结

- 认识最基本的 PE 程序结构，定位 `main`；
- 从 `.rdata` 中读取字符数组并还原成字符串；
- 签到题先跑再逆向的思路。
