#!/bin/sh
# 新手课堂：FLAG 由平台运行时注入（-e FLAG=...），应用内 os.environ 读取
exec python -m uvicorn main:app --host 0.0.0.0 --port 80
