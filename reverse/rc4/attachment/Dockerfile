FROM debian:bookworm AS builder

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc-mingw-w64-x86-64 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build
COPY rc4.c .
RUN x86_64-w64-mingw32-gcc -O2 -s -Wall -Wextra -o /build/rc4.exe rc4.c

FROM debian:bookworm-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends wine \
    && rm -rf /var/lib/apt/lists/*

ENV WINEDEBUG=-all
WORKDIR /app
COPY --from=builder /build/rc4.exe /app/rc4.exe

CMD ["wine", "/app/rc4.exe"]
