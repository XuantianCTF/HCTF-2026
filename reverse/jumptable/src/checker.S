.intel_syntax noprefix
.global _start

.text

_start:
    mov rcx, QWORD PTR [rsp+16]

    xor eax, eax
    mov al, BYTE PTR [rcx]

    lea rdx, [jump_table]
    mov rax, QWORD PTR [rdx + rax*8]
    jmp rax

success:
    mov BYTE PTR [rsp], 0x2f     # '/'
    mov BYTE PTR [rsp+1], 0x66   # 'f'
    mov BYTE PTR [rsp+2], 0x6c   # 'l'
    mov BYTE PTR [rsp+3], 0x61   # 'a'
    mov BYTE PTR [rsp+4], 0x67   # 'g'
    mov BYTE PTR [rsp+5], 0x00   # '\0'

    # 1. Syscall: open("/flag", O_RDONLY)
    mov rdi, rsp
    mov rsi, 0
    mov rax, 2
    syscall

    mov rdi, rax
    mov rsi, rsp                 # 复用 rsp 栈空间作为 buf 接收 flag
    mov rdx, 0x40                # 读取 64 字节
    mov rax, 0                   # syscall 编号 0 (sys_read)
    syscall

    # 3. Syscall: write(1, buf, len)
    mov rdx, rax                 # 实际读取的字节数作为长度
    mov rdi, 1                   # stdout
    mov rax, 1                   # syscall 编号 1 (sys_write)
    syscall

    # 4. Syscall: exit(0)
    xor edi, edi
    mov rax, 60                  # syscall 编号 60 (sys_exit)
    syscall

# ==========================================
# 失败分支：直接退出
# ==========================================
fail:
    mov rax, 60                  # sys_exit
    mov rdi, 1                   # 退出码 1
    syscall

# ==========================================
# 纯手工跳转表 (硬核查表逻辑)
# ==========================================
# 紧跟在代码段后面，这样 objdump 就会将其当作指令反汇编，
# 产生你题目中看到的形如 "75 10 40 00" 的混淆效果。
jump_table:
    # 假设正确的字符是 'k' (ASCII 码 107)
    # 我们填充 256 个表项，涵盖所有单字节可能性

    .rept 107                    # 前 107 个元素 (0 ~ 106)
    .quad fail
    .endr

    .quad success                # 第 108 个元素 (ASCII 107) -> 指向成功

    .rept 148                    # 剩下的 148 个元素 (108 ~ 255)
    .quad fail
    .endr

.section .note.GNU-stack,"",@progbits
