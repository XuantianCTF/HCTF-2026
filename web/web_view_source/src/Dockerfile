# web_view_source deployment image (internal, do NOT publish to players)
# 纯 Python 3 标准库实现，无外部依赖，alpine 足够。
FROM python:3.12-alpine

WORKDIR /app
COPY server.py index.html ./

# 动态 flag：平台在容器启动时注入 FLAG，server.py 会把它写进 HTML 注释。
# 这里故意不设置，方便发现平台漏注入。
EXPOSE 8080

CMD ["python3", "server.py"]
