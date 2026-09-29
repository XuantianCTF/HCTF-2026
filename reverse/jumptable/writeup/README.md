# jumptable Writeup

## 0. 拿到附件

附件是 `checker.S`（`.intel_syntax noprefix`），CI 会把它编译成静态 ELF。
线上环境可以直接 SSH 进去，里面有 `gdb` / `objdump` / `strace`：

```bash
ssh ctf@<host> -p 22     # 密码 ctf
file /home/ctf/checker
objdump -d /home/ctf/checker | less
```

## 1. 观察入口

`_start` 的逻辑很短：

```asm
_start:
    mov rcx, QWORD PTR [rsp+16]   ; rsp+16 = argv[1]
    xor eax, eax
    mov al, BYTE PTR [rcx]        ; 只取 argv[1] 的第 1 个字节
    lea rdx, [jump_table]
    mov rax, QWORD PTR [rdx + rax*8]
    jmp rax
```

进程刚进入 `_start` 时栈布局是 `argc / argv[0] / argv[1] / ...`，所以
`[rsp+16]` 就是 `argv[1]`。程序只看它的**第一个字节**，然后用它当索引去
`jump_table` 里取一个函数地址，再 `jmp` 过去。

## 2. 看穿“混淆”的跳转表

`jump_table` 紧跟在 `.text` 里，`objdump` 会把这些 8 字节地址当成指令：

```asm
...
  4010xx:  75 10 40 00 00 00 00 00   jne ...
  4010xx:  75 10 40 00 00 00 00 00   jne ...
  ...
```

其实每一项都是一个 `.quad`。表一共 256 项，结构是：

```asm
jump_table:
    .rept 107
    .quad fail
    .endr
    .quad success        ; 第 0x6b = 107 项
    .rept 148
    .quad fail
    .endr
```

所以只有索引 `107`（也就是 ASCII 的 `'k'`）指向 `success`，其余全是指向 `fail`。
在 `gdb` 里也很直观：

```bash
gdb -q /home/ctf/checker
(gdb) b *(_start+... )   # 停在 jmp rax 之前
(gdb) run a
(gdb) p/x $rax           # 0x4010xx，用 x/i 看它落到哪个函数
```

## 3. success 分支

```asm
success:
    mov BYTE PTR [rsp], 0x2f     # '/'
    mov BYTE PTR [rsp+1], 0x66   # 'f'
    mov BYTE PTR [rsp+2], 0x6c   # 'l'
    mov BYTE PTR [rsp+3], 0x61   # 'a'
    mov BYTE PTR [rsp+4], 0x67   # 'g'
    mov BYTE PTR [rsp+5], 0x00   # '\0'
    ; open("/flag", O_RDONLY) ; read ; write(1, ...) ; exit
```

它在栈上拼出 `"/flag\0"`，`open` → `read` → `write` 到 stdout。
`/flag` 权限是 `root:root 0400`，而 `/home/ctf/checker` 是 setuid root，所以
只有通过这个程序才能读到动态 flag。

## 4. 拿 flag

```bash
/home/ctf/checker k        # 任意以 'k' 开头的参数都可以
# HCTF{...}
```

## 5. 本地复现

```bash
docker build -t rev-jumptable ./attachment
printf 'HCTF{jump_table_g4t3_1s_n0t_0p4qu3}\n' > flag
docker run --rm -v "$PWD/flag:/flag:ro" rev-jumptable k_whatever
```

## 考点小结

- 从 `_start` 的栈布局还原出“读 `argv[1]`”；
- 识别 `.text` 中被伪装成指令的地址表（`jmp rax` 跳转表）；
- 用 `gdb` / `objdump` 动态定位唯一成功分支；
- 理解 setuid + 受限 `/flag` 的读取链路。
