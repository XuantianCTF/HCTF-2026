# 单容器部署：nginx 网关 + FastAPI 后端同容器（平台一题一容器）
FROM python:3.11-slim

RUN apt-get update     && apt-get install -y --no-install-recommends nginx     && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.org/simple
COPY backend/ .
RUN python seed.py

COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY frontend /usr/share/nginx/html

EXPOSE 80
ENTRYPOINT ["./entrypoint.sh"]
