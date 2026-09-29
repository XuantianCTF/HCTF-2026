FROM ubuntu:22.04 AS builder

RUN apt-get update \
    && apt-get install -y --no-install-recommends binutils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build
COPY checker.S .
RUN as --64 -o checker.o checker.S \
    && ld -o checker checker.o -z noexecstack \
    && rm -f checker.o

FROM alpine:3.19

WORKDIR /app
COPY --from=builder /build/checker /app/checker
RUN chmod +x /app/checker

ENTRYPOINT ["/app/checker"]
