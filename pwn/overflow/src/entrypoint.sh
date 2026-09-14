#!/bin/sh
set -e

if [ -n "$FLAG" ]; then
    printf '%s\n' "$FLAG" > /flag
else
    printf '%s\n' 'flag{this_is_a_demo_flag}' > /flag
fi

exec socat TCP-LISTEN:9999,reuseaddr,fork EXEC:/app/vuln
