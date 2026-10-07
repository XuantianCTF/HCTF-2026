# web_hidden_api deployment image (internal, do NOT publish to players)
# 纯 Python 3 标准库实现，无外部依赖，alpine 足够。
FROM python:3.12-alpine

WORKDIR /app
COPY server.py index.html app.js ./

# 动态 flag：平台在容器启动时注入 FLAG，/api/v2/backup 校验 key 后返回。
# 这里故意不设置，方便发现平台漏注入。
EXPOSE 8082

CMD ["python3", "server.py"]
