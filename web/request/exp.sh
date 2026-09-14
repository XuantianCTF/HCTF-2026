curl -X OPTIONS http://localhost:58000/                    # 获取 hints
curl -X POST http://localhost:58000/ \
  -H "X-Forwarded-For: 127.0.0.1" \
  -H "User-Agent: Mozilla/5.0 (compatible; ImpostorBot/1.0)" \
  -H "Referer: https://admin.internal.ctf/login"
