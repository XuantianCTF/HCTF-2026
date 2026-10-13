# 新手课堂：PPT 式 Web 入门引导题（纯 FastAPI 单服务，无 nginx）
FROM python:3.12-alpine

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.org/simple

COPY main.py entrypoint.sh ./
COPY lessons/ lessons/
COPY static/ static/

RUN chmod +x entrypoint.sh
# 默认 FLAG 必须是恰好 5 段下划线分隔（与平台 checker 的 TEMPLATE 对应）
ENV FLAG="HCTF{we1c0me_t0_web_ctf_2026}"
EXPOSE 80
ENTRYPOINT ["./entrypoint.sh"]
