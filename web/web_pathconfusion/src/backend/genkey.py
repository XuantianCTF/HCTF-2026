#!/usr/bin/env python3
"""生成题目专用 RSA-1024 密钥对（脱敏：不使用线上真实私钥），并生成密文与补丁。

输出:
  keys.json        - {modulus, public_exponent, private_exponent}（hex，与 app.js 常量同格式）
  token_sample.txt - TAG+timestamp 的 RSA 加密样例（模拟拦截到的登录密文，题2素材）
"""
import json
import time
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from Crypto.Util.number import bytes_to_long, long_to_bytes

OUT = Path(__file__).parent

# ---- 生成 1024bit 密钥对 ----
key = rsa.generate_private_key(public_exponent=65537, key_size=1024)
priv = key.private_numbers()
n = priv.public_numbers.n
e = priv.public_numbers.e
d = priv.d

def hexfmt(x: int, width: int = 256) -> str:
    h = format(x, "x")
    h = h.zfill(width)
    if len(h) % 2:
        h = "0" + h
    return h

keys = {
    "modulus": hexfmt(n),
    "public_exponent": hexfmt(e, 6),
    "private_exponent": hexfmt(d),
}
(OUT / "keys.json").write_text(json.dumps(keys, indent=2))

# ---- 复现前端 token 加密逻辑（RSA/None/PKCS1-v1_5，明文 = TAG + 时间戳毫秒） ----
from Crypto.Cipher import PKCS1_v1_5 as _p  # noqa: E402
from Crypto.PublicKey import RSA as _rsa  # noqa: E402

TAG = "cas"
plain = TAG + str(int(time.time() * 1000))
pub = _rsa.construct((n, e))
cipher = _p.new(pub)
ct = cipher.encrypt(plain.encode())
(OUT / "token_sample.txt").write_text(ct.hex())

print("modulus          :", keys["modulus"][:32], "...")
print("public_exponent  :", keys["public_exponent"])
print("private_exponent :", keys["private_exponent"][:32], "...")
print("token sample     :", ct.hex()[:64], "...")
