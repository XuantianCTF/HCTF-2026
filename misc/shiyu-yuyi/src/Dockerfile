# 时雨羽衣 · 选手自开容器
# 平台启动时注入 FLAG=HCTF{8-4-4-4-12}。不要把真 flag 写进镜像。
# 模型密钥走环境变量 LLM_API_KEY，由平台 environ 注入，不进镜像层。
ARG PYTHON_IMAGE=python:3.12-slim
FROM ${PYTHON_IMAGE}

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    LLM_BASE_URL=https://api.deepseek.com \
    LLM_MODEL=deepseek-flash \
    LLM_THINKING=disabled \
    LLM_HEALTH_PROVIDER=https://api.deepseek.com

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && useradd --create-home --uid 10001 ctf

COPY app.py OIP-C.webp ./
COPY templates ./templates

RUN chown -R ctf:ctf /app
USER ctf

EXPOSE 8000
CMD ["gunicorn", "-w", "1", "--threads", "8", "-b", "0.0.0.0:8000", "--timeout", "90", "--access-logfile", "-", "app:app"]
