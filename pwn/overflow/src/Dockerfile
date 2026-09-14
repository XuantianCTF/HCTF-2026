FROM ubuntu:22.04 AS builder

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libc6-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build
COPY vuln.c .
RUN gcc vuln.c -o vuln -fno-stack-protector -no-pie -O0 -g

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends socat \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /build/vuln /app/vuln
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/vuln /app/entrypoint.sh

EXPOSE 9999

CMD ["/app/entrypoint.sh"]
