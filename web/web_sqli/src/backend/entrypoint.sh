#!/bin/sh
# 动态 FLAG：平台注入 FLAG 时启动重播种（flag 写入管理员公告）
if [ -n "$FLAG" ]; then
    python seed.py
fi
python -m uvicorn app:app --host 127.0.0.1 --port 8000 &
exec nginx -g 'daemon off;'
