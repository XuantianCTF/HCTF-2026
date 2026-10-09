FROM debian:bookworm AS builder

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc-mingw-w64-x86-64 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build
COPY signin.c .
RUN x86_64-w64-mingw32-gcc -O2 -static -o signin.exe signin.c

FROM debian:bookworm-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends wine \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /build/signin.exe /app/signin.exe

CMD ["wine", "/app/signin.exe"]
