#!/bin/sh
set -eu

: "${FLAG:=HCTF{local_test_flag}}"
printf '%s\n' "$FLAG" > /flag
chown root:root /flag
chmod 400 /flag

# 不要把动态 flag 留在环境里，避免 SSH 用户在子进程/会话中读到
unset FLAG

ssh-keygen -A

exec /usr/sbin/sshd -D -e
