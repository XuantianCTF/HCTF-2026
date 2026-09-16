# kan-yi-dao deployment image (internal, do NOT publish to players)
# Python 3 stdlib only - alpine is sufficient, no external dependencies.
FROM python:3.12-alpine

WORKDIR /app
COPY server.py index.html ./

# Dynamic flag: the platform injects FLAG at container start (overrides the
# in-code fallback). Not set here on purpose so a missing injection is visible.
EXPOSE 8931

CMD ["python3", "server.py"]
