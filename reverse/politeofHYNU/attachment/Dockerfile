FROM ubuntu:22.04 AS builder
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc make libc6-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
COPY . /src/
RUN make && mkdir -p /build && cp client.elf server.elf /build/
