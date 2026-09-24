# -*- coding: utf-8 -*-
"""生成 cas.db：1000 名虚拟师生（含管理员 userId=1、目标学生 Neeco）。

字段全部为程序生成的假数据；FLAG3 藏于 Neeco.description。
同时把"拦截到的登录密文"写入 data/captured_login.txt（题 2 素材，doc.html 与
题目附件共用同一份）。
"""
import json
import os
import random
import sqlite3
import string
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric import rsa
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

BASE = Path(__file__).parent
DATA = BASE / "data"
DATA.mkdir(exist_ok=True)
DB = DATA / "cas.db"

# 独立部署版（headerauth）：本题只需 FLAG3（Neeco 档案）；题2 的密文解出
# 口令已替换为无害占位符——假密码，非 flag。
FLAG3 = os.environ.get("FLAG") or os.environ.get("FLAG3", "hctf{h34d3r_1nj3ct10n_pwn3d_all}")
FLAG2 = os.environ.get("FLAG2", "Admin@demo2026#Test")

SURNAMES = "王李张刘陈杨黄赵周吴徐孙马朱胡郭何高林郑谢罗梁宋唐许韩冯邓曹彭曾肖田董袁潘蒋蔡余杜叶程苏魏吕丁任沈姚卢姜崔钟谭陆汪范金石廖贾夏韦付方白邹孟熊秦邱江尹薛闫段雷侯龙史陶黎贺顾毛郝龚邵万钱严覃武戴莫孔向汤"
GIVEN = [
    "志强", "伟", "明", "磊", "军", "洋", "勇", "艳", "杰", "娟", "涛", "明",
    "超", "秀英", "霞", "平", "刚", "桂英", "文静", "丽", "强", "超", "军",
    "慧", "巧", "淑兰", "静", "敏", "芳", "燕", "婷", "雪", "欣怡", "梓涵",
    "雨轩", "子豪", "宇轩", "浩然", "一诺", "奕辰", "嘉懿", "致远", "天佑",
    "昊天", "思远", "博", "晨曦", "若曦", "芷晴", "语嫣", "佳琪", "睿",
]
ORGS = [
    (1, "计算机学院", "计算机科学与技术"),
    (2, "机械工程学院", "机械设计制造及其自动化"),
    (3, "电气工程学院", "电气工程及其自动化"),
    (4, "经济管理学院", "国际经济与贸易"),
    (5, "语言文学学院", "汉语言文学"),
    (6, "数理学院", "信息与计算科学"),
]
GRADES = ["2022", "2023", "2024", "2025"]
CAMPUSES = ["东校区", "西校区"]


def rand_name(rng):
    return rng.choice(SURNAMES) + rng.choice(GIVEN)


def rand_phone(rng):
    return "1" + rng.choice("3578") + "".join(rng.choice(string.digits) for _ in range(9))


def hexid(rng, n=16):
    return "".join(rng.choice("0123456789abcdef") for _ in range(n))


FIELDS = [
    "userId", "userName", "account", "sex", "orgId", "orgName", "grade",
    "professional", "className", "status",
    "nation", "political", "idCard", "birthday", "nativePlace", "phone",
    "email", "qq", "wechat", "dormitory", "address", "emergencyContact",
    "emergencyPhone", "enrollDate", "enrollType", "studentType", "length",
    "campus", "building", "cardNo", "bankCard", "bankName", "scholarship",
    "loan", "award", "punish", "cet4", "cet6", "computer", "teacher",
    "counselor", "password", "salt", "createTime", "updateTime", "lastLogin",
    "loginCount", "source", "remark", "tag", "version", "deleted", "secretLevel",
    "description",
]


def make_row(rng, uid, name, org, grade, is_admin=False, is_transfer=False):
    org_id, org_name, prof = org
    acct = f"{grade}{org_id:02d}{rng.randint(1, 999):03d}"
    row = {
        "userId": str(uid),
        "userName": name,
        "account": acct,
        "sex": rng.choice(["男", "女"]),
        "orgId": org_id if not is_admin else -1,
        "orgName": "系统管理员" if is_admin else org_name,
        "grade": "教职工" if is_admin else grade,
        "professional": "信息中心" if is_admin else prof,
        "className": "-" if is_admin else f"{grade}级{prof[:2]}{rng.randint(1, 6)}班",
        "status": 1,
        "nation": rng.choice(["汉族", "汉族", "汉族", "回族", "满族"]),
        "political": rng.choice(["共青团员", "共青团员", "中共党员", "群众"]),
        "idCard": f"11{rng.randint(10, 99)}0{rng.randint(1970, 2007):04d}{rng.randint(1, 12):02d}{rng.randint(1, 28):02d}{rng.randint(1000, 9999)}{rng.choice(string.digits)}X",
        "birthday": f"{rng.randint(1970, 2007)}-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}",
        "nativePlace": rng.choice(["北京海淀", "上海浦东", "广东广州", "四川成都", "浙江杭州", "江苏南京"]),
        "phone": rand_phone(rng),
        "email": f"stu{acct}@example.edu.cn",
        "qq": str(rng.randint(10000, 999999999)),
        "wechat": f"wx_{hexid(rng, 8)}",
        "dormitory": "-" if is_admin else f"{rng.choice(CAMPUSES[:1])}{rng.randint(1, 30)}栋{rng.randint(100, 699)}",
        "address": rng.choice(["示例市示范区学院路1号", "示例市高新区智慧大道8号", "示例市城区信息路66号"]),
        "emergencyContact": rand_name(rng),
        "emergencyPhone": rand_phone(rng),
        "enrollDate": f"{grade}-09-01" if not is_admin else "2018-03-01",
        "enrollType": "插班生" if is_transfer else rng.choice(["普通高考", "普通高考", "专升本", "转专业"]),
        "studentType": "本科生",
        "length": 4,
        "campus": rng.choice(CAMPUSES),
        "building": f"{rng.choice(['一', '二', '三', '四'])}教学楼",
        "cardNo": f"10{acct}",
        "bankCard": f"62{rng.randint(100, 999)}{rng.randint(10 ** 14, 10 ** 15)}",
        "bankName": rng.choice(["中国工商银行", "中国建设银行", "中国银行"]),
        "scholarship": rng.choice(["国家励志奖学金", "校三等奖学金", "-", "-", "-"]),
        "loan": rng.choice(["生源地贷款", "-", "-", "-"]),
        "award": rng.choice(["校三好学生", "院优秀学生干部", "-", "-"]),
        "punish": rng.choice(["-", "-", "-", "-", "警告处分(已解除)"]),
        "cet4": rng.choice(["425", "478", "512", "-", "531"]),
        "cet6": rng.choice(["-", "-", "456", "489"]),
        "computer": rng.choice(["二级C语言", "二级Python", "-", "-"]),
        "teacher": rand_name(rng),
        "counselor": rand_name(rng),
        "password": hexid(rng, 32),
        "salt": hexid(rng, 8),
        "createTime": f"{int(grade) - 1}-09-05 10:{rng.randint(10, 59)}:{rng.randint(10, 59)}" if not is_admin else "2018-03-01 09:00:00",
        "updateTime": "2026-08-30 15:20:11",
        "lastLogin": f"2026-09-{rng.randint(1, 14):02d} {rng.randint(8, 22):02d}:{rng.randint(10, 59):02d}:{rng.randint(10, 59):02d}",
        "loginCount": rng.randint(1, 400),
        "source": "迎新系统",
        "remark": "-" if not is_transfer else "2025年春季插入2023级，学籍异动已备案",
        "tag": "插班生" if is_transfer else "",
        "version": rng.randint(1, 9),
        "deleted": 0,
        "secretLevel": 2,
        "description": "-" if not is_transfer else (
            "插班生档案（涉密）。奖励核查通过后发放迎新系统兑换码："
            + FLAG3
        ),
    }
    return row


def main():
    rng = random.Random(20260916)
    rows = [make_row(rng, 1, "系统管理员", ORGS[0], "2022", is_admin=True)]
    uid = 100
    for i in range(1000):
        uid += rng.randint(1, 4)
        org = rng.choice(ORGS)
        grade = rng.choice(GRADES)
        rows.append(make_row(rng, uid, rand_name(rng), org, grade))
    # 目标：插班生 Neeco（userId 固定为 20258888，便于核对）
    rows.append(make_row(rng, 20258888, "Neeco", ORGS[0], "2023", is_transfer=True))

    if os.path.exists(DB):
        os.remove(DB)
    conn = sqlite3.connect(DB)
    conn.execute(f"CREATE TABLE users ({', '.join(f'{f} TEXT' for f in FIELDS)})")
    conn.executemany(
        f"INSERT INTO users ({', '.join(FIELDS)}) VALUES ({', '.join('?' * len(FIELDS))})",
        [tuple(r[f] for f in FIELDS) for r in rows],
    )
    conn.commit()
    conn.close()
    print(f"seeded {len(rows)} users -> {DB}")

    # ---- 题目 2 素材：用 app.js 内的公钥加密 TAG+时间戳，作为"拦截密文" ----
    keys = json.load(open(BASE / "keys.json"))
    n = int(keys["modulus"], 16)
    e = int(keys["public_exponent"], 16)
    pub = RSA.construct((n, e))
    # 联调抓包：管理员测试账号的口令即 FLAG2（RSA/None/PKCS1-v1_5 加密）
    ct = PKCS1_v1_5.new(pub).encrypt(FLAG2.encode()).hex()
    (DATA / "captured_login.txt").write_text(ct)
    print(f"captured ciphertext -> {DATA / 'captured_login.txt'} ({len(ct)} hex chars)")


if __name__ == "__main__":
    main()
