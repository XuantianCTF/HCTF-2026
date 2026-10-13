#!/usr/bin/env python3

KEY = b"hctf2026_standard_rc4"
CIPHERTEXT = bytes.fromhex(
    "624ac1dd81960f32a224ecbdfa72affacef7ec8e083749a547b3869e"
)


def rc4(key: bytes, data: bytes) -> bytes:
    state = list(range(256))
    j = 0

    for i in range(256):
        j = (j + state[i] + key[i % len(key)]) & 0xff
        state[i], state[j] = state[j], state[i]

    output = bytearray()
    i = j = 0
    for value in data:
        i = (i + 1) & 0xff
        j = (j + state[i]) & 0xff
        state[i], state[j] = state[j], state[i]
        output.append(value ^ state[(state[i] + state[j]) & 0xff])
    return bytes(output)


if __name__ == "__main__":
    print(rc4(KEY, CIPHERTEXT).decode())
