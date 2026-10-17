#!/bin/bash
set -euo pipefail

# Dynamic flag: the platform injects FLAG at container start.
if [ -n "${FLAG:-}" ]; then
    printf '%s\n' "$FLAG" > /root/flag.txt
else
    printf '%s\n' 'HCTF{demo_flag_for_local_test}' > /root/flag.txt
fi
chmod 600 /root/flag.txt

service cron start
exec /usr/sbin/sshd -D -e
