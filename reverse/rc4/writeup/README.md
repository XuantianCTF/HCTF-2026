# rc4 Writeup

## 分析思路

程序读取输入后用内置密钥运行 RC4，再与内置密文逐字节比较。分析二进制中的两个常量和 RC4 实现：

- 密钥：`hctf2026_standard_rc4`
- 密文：`624ac1dd81960f32a224ecbdfa72affacef7ec8e083749a547b3869e`
- KSA 将状态初始化为 `0..255`，并执行 256 轮标准密钥调度。
- PRGA 每轮更新 `i`、`j`，交换 `S[i]` 和 `S[j]`，取出密钥流字节并与输入异或。

RC4 的加密和解密相同。将密文作为输入再次运行标准 RC4，即可还原 flag：

```bash
python3 exp.py
# HCTF{rc4_is_a_stream_cipher}
```

将还原出的 flag 输入附件程序会得到 `Correct!`。

## Flag

```text
HCTF{rc4_is_a_stream_cipher}
```
