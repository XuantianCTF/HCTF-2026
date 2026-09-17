# ezgo Writeup

## 定位校验逻辑

Go 二进制默认保留符号表，用 `go tool nm`、Ghidra 或 IDA 都能直接看到函数名：

```bash
go tool nm attachment/ezgo | grep -i main
```

其中 `main.check` 就是 flag 校验函数。

## 分析 check

反编译后核心逻辑如下：

```go
var secret = []byte{
    0x2f, 0x2c, 0x24, 0x2e, 0x1e, 0x15, 0x57, 0x03, 0x11, 0x06, 0x02,
    0x2d, 0x1f, 0x5f, 0x02, 0x37, 0x54, 0x01, 0x38, 0x0a, 0x0a, 0x15,
}

var key = "gopher"

func check(flag string) bool {
    if len(flag) != len(secret) {
        return false
    }
    for i := 0; i < len(secret); i++ {
        if flag[i]^key[i%len(key)] != secret[i] {
            return false
        }
    }
    return true
}
```

密钥是字符串常量 `gopher`，密文是 `secret` 字节数组，长度 22。

## 解密

异或是对称运算，直接 `secret[i] ^ key[i % len(key)]` 即可还原：

```python
secret = [0x2f, 0x2c, 0x24, 0x2e, 0x1e, 0x15, 0x57, 0x03, 0x11, 0x06, 0x02,
          0x2d, 0x1f, 0x5f, 0x02, 0x37, 0x54, 0x01, 0x38, 0x0a, 0x0a, 0x15]
key = b"gopher"
flag = bytes(secret[i] ^ key[i % len(key)] for i in range(len(secret))).decode()
print(flag)
```

得到：

```
HCTF{g0lang_x0r_1s_ez}
```

## 验证

```bash
python3 exp.py                # 自动读取 ../attachment/ezgo 验证
# 或手动
echo 'HCTF{g0lang_x0r_1s_ez}' | ./attachment/ezgo
# Correct! You are a Go reverser now :)
```
