#!/bin/sh
# 支持动态 FLAG：平台注入 FLAG，或本地联调用 FLAG1/FLAG2/FLAG3（重建数据库与密文）
if [ -n "$FLAG" ] || [ -n "$FLAG1" ] || [ -n "$FLAG2" ] || [ -n "$FLAG3" ]; then
    python seed.py
fi
python -m uvicorn app:app --host 127.0.0.1 --port 8000 &
exec nginx -g 'daemon off;'
