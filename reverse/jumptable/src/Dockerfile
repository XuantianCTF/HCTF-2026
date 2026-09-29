FROM ubuntu:22.04 AS builder

RUN apt-get update \
    && apt-get install -y --no-install-recommends binutils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build
COPY checker.S .
RUN as --64 -o checker.o checker.S \
    && ld -o checker checker.o -z noexecstack \
    && rm -f checker.o

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        openssh-server \
        gdb \
        binutils \
        file \
        strace \
        ltrace \
        vim \
        less \
        python3 \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash ctf \
    && echo 'ctf:ctf' | chpasswd \
    && mkdir -p /run/sshd

COPY --from=builder /build/checker /home/ctf/checker
RUN chown root:root /home/ctf/checker \
    && chmod 4755 /home/ctf/checker

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 22
CMD ["/entrypoint.sh"]
