#!/usr/bin/env python3
"""扮演 Server，与容器里的 Client 握手拿动态 flag。
用法: python solve.py [host] [port]
"""
import socket
import sys

MAGIC = b"PxTL"
KEY = bytes.fromhex("1bab71b8117f4dea")
WELCOME_XOR = 0x5A
CMD_HELLO, CMD_WELCOME, CMD_AUTH, CMD_PROOF, CMD_GRANT, CMD_ERROR = (
    0xA1, 0xA2, 0xA3, 0xA4, 0xA5, 0xEE,
)


def cksum(buf: bytes) -> int:
    c = 0
    for b in buf:
        c ^= b
    return c


def pkt(cmd: int, seq: int, data: bytes = b"") -> bytes:
    if len(data) > 128:
        raise ValueError("payload too long")
    body = MAGIC + bytes([cmd, seq, len(data)]) + data
    return body + bytes([cksum(body)])


def recvn(sock: socket.socket, n: int) -> bytes:
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("closed, got %r" % buf)
        buf += chunk
    return buf


def recvp(sock: socket.socket):
    hdr = recvn(sock, 7)
    if hdr[:4] != MAGIC:
        raise ValueError("bad magic: %r" % hdr)
    cmd, seq, length = hdr[4], hdr[5], hdr[6]
    data = recvn(sock, length) if length else b""
    ck = recvn(sock, 1)[0]
    if ck != cksum(hdr + data):
        raise ValueError("bad checksum")
    return cmd, seq, data


def solve(host: str, port: int) -> str:
    sock = socket.create_connection((host, port), timeout=10)
    try:
        cmd, seq, hello = recvp(sock)
        if cmd == CMD_ERROR:
            raise RuntimeError("error: %s" % hello.decode("latin1"))
        if cmd != CMD_HELLO or seq != 0 or len(hello) != 9:
            raise RuntimeError("unexpected hello: cmd=%r seq=%r data=%r" % (cmd, seq, hello))
        mode = hello[0]
        nonce_c = hello[1:5]
        if hello[5:] != b"HELO":
            raise RuntimeError("bad helo marker")
        if mode != 0x52:
            raise RuntimeError("expect remote mode 'R', got %r" % mode)

        nonce_s = b"\x11\x22\x33\x44"
        echo = bytes(b ^ WELCOME_XOR for b in nonce_c)
        sock.sendall(pkt(CMD_WELCOME, 1, nonce_s + echo + b"WELC"))

        cmd, seq, chal = recvp(sock)
        if cmd == CMD_ERROR:
            raise RuntimeError("welcome rejected: %s" % chal.decode("latin1"))
        if cmd != CMD_AUTH or seq != 2 or len(chal) != 8:
            raise RuntimeError("unexpected auth: cmd=%r seq=%r data=%r" % (cmd, seq, chal))

        mix = nonce_c + nonce_s
        proof = bytes(c ^ k ^ m for c, k, m in zip(chal, KEY, mix))
        sock.sendall(pkt(CMD_PROOF, 3, proof))

        cmd, seq, flag = recvp(sock)
        if cmd == CMD_ERROR:
            raise RuntimeError("proof rejected: %s" % flag.decode("latin1"))
        if cmd != CMD_GRANT or seq != 4:
            raise RuntimeError("unexpected grant: cmd=%r seq=%r data=%r" % (cmd, seq, flag))
        return flag.decode()
    finally:
        sock.close()


if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 9999
    print(solve(host, port))
