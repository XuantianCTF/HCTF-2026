# overflow Writeup

## 漏洞点

`vuln()` 中使用 `gets(buf)` 读取输入，且 `buf` 只有 64 字节，没有任何长度限制，存在典型的栈溢出。

二进制编译参数为 `-fno-stack-protector -no-pie`，因此：

- 没有栈 Canary，可以随意覆盖返回地址；
- 没有 PIE，函数地址固定，可以直接硬编码。

程序中还存在一个永远不会被调用的 `win()` 函数，它会执行 `system("cat /flag")`。

## 利用思路

覆盖 `vuln()` 的返回地址为 `win()` 的地址，即 ret2win。

栈布局：

```
+----------------+  <- rbp + 0x08  返回地址
|  saved rbp     |  <- rbp
+----------------+
|  buf[64]       |  <- rbp - 0x40
+----------------+
```

因此 padding 长度为 `64 + 8 = 72`。

## 利用脚本

```bash
python3 exp.py                      # 本地
python3 exp.py remote <host> <port> # 远程
```

脚本会用 pwntools 解析 `win` 符号地址，发送 `72 * 'A' + p64(win)`，随后即可拿到 shell 并读取 `/flag`。
