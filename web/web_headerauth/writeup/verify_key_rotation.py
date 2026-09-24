#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证 headerauth 实例的私钥轮换：旧密文不可解、原密钥可解（对照组）。"""
import json
import re
from pathlib import Path

from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

base = Path(__file__).parent.parent / "src"
keys = json.loads((base / "backend" / "keys.json").read_text())
n = int(keys["modulus"], 16)
e = int(keys["public_exponent"], 16)
old_d = int(keys["private_exponent"], 16)

js = (base / "frontend" / "assets" / "js" / "app.205f0432cfa79c504913.js").read_text(encoding="utf-8")
m = re.search(r'private_exponent:"([0-9a-fA-F]+)"', js)
assert m, "private_exponent hex not found in app.js"
new_d = int(m.group(1), 16)  # JS 常量可能带额外前导零，按整数值比较
print("app.js 中的 d 与 keys.json 原 d 相同?", new_d == old_d)

ct = PKCS1_v1_5.new(RSA.construct((n, e))).encrypt(b"hctf{test}")
c = int.from_bytes(ct, "big")
k = 128

mb = pow(c, new_d, n).to_bytes(k, "big")
print("轮换 d 解密 PKCS1 padding 有效?", mb[0] == 0 and mb[1] == 2)

mb2 = pow(c, old_d, n).to_bytes(k, "big")
plain = mb2[mb2.index(0, 2) + 1:]
print("原 d 解密恢复明文?", plain == b"hctf{test}")
