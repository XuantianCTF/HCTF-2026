#!/usr/bin/env python3
import os
import subprocess
import sys

SUCCESS_INDEX = 0x6B                 # ASCII 'k'
DEMO_FLAG = "HCTF{jump_table_g4t3_1s_n0t_0p4qu3}"
IMAGE = "rev-jumptable"


def analyze():
    key = chr(SUCCESS_INDEX)
    print(f"[+] jump_table[0x{SUCCESS_INDEX:02x}] -> success")
    print(f"[+] argv[1] must start with {key!r}")
    return key


def verify_docker(key):
    here = os.path.dirname(os.path.abspath(__file__))
    flag = os.path.join(here, "flag.tmp")
    with open(flag, "w") as f:
        f.write(DEMO_FLAG + "\n")
    try:
        out = subprocess.run(
            ["docker", "run", "--rm", "-v", f"{flag}:/flag:ro", IMAGE, key + "_demo"],
            capture_output=True, text=True, timeout=60,
        )
        print("[+] stdout:", out.stdout.strip())
        print("[+] verify:", DEMO_FLAG in out.stdout)
    except FileNotFoundError:
        print("[!] docker not found")
    finally:
        os.unlink(flag)


def main():
    key = analyze()
    if "--docker" in sys.argv:
        verify_docker(key)
    else:
        print("[i] online : ssh ctf@<host> -p 22        # password: ctf")
        print(f"[i] then  : /home/ctf/checker {key}")
        print("[i] local : docker build -t rev-jumptable ../attachment")
        print(f"[i]         docker run --rm -v $PWD/flag:/flag:ro rev-jumptable {key}")
        print("[i] pass --docker to verify automatically")


if __name__ == "__main__":
    main()
