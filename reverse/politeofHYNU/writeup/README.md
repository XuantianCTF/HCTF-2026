# 题解 · 不是这个 Flag

## 0. 诱饵

```text
$ strings client.elf | grep HCTF
HCTF{1bab71b8-117f-4dea-a047-340b72101d7b}
```

本地把 `server.elf` 和 `client.elf` 跑起来也会打出这一串。交平台是错的，这是模板。

## 1. 本地先看对话

```text
./server.elf 2333
./client.elf 127.0.0.1 2333
```

或直接 `nc` 抓第一包：

```text
$ nc host 9999 | xxd
00000000: 5078 544c a100 094c ....              PxTL....
```

帧格式：

```
magic "PxTL" | cmd 1B | seq 1B | len 1B | data | cksum(前面全字节 XOR)
```

Client 先发 `cmd=0xA1` HELLO。你要当 Server 往下接。

## 2. 握手

`main`：`do_hello` → `do_auth` → `send_grant`。

### HELLO / WELCOME

HELLO data：`[mode][nonce_c 4][HELO]`

- 附件互聊 `mode='L'`
- 容器 stdio `mode='R'`（`0x52`）

你回 `cmd=0xA2` seq=1，12 字节：

```
nonce_s(4)  +  nonce_c[i]^0x5A  +  "WELC"
```

### AUTH / PROOF

`build_key` 从模板 `HCTF{` 后面取出 UUID，跳过 `-`，hex 解码。前 8 字节：

```
1bab71b8117f4dea  ->  1b ab 71 b8 11 7f 4d ea
```

Client 发 8 字节随机 `chal`（`cmd=0xA3` seq=2）。你回 `cmd=0xA4` seq=3：

```
mix = nonce_c || nonce_s
proof[i] = chal[i] ^ key[i] ^ mix[i]
```

过了之后 Client 发 `cmd=0xA5` GRANT，里面是这份实例的真 flag（`FLAG` / `/flag`，否则容器启动时生成的 `HCTF{uuid}`）。

附件自带的 `server.elf` 只吃 `'L'` 且只打印模板，不能直接 socat 到远端。

## 3. 脚本

见 `tools/solve.py`。本地验收：打出 `HCTF{随机uuid}`，和 strings 模板不是同一个。
