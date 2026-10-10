FROM ubuntu:22.04 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc make libc6-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
COPY . /src/
RUN make && gcc -O2 -Wall -o /wrap wrap.c

FROM ubuntu:22.04
COPY --from=build /src/client.elf /app/client.elf
COPY --from=build /src/server.elf /app/server.elf
COPY --from=build /wrap /app/wrap
RUN chmod +x /app/client.elf /app/server.elf /app/wrap
WORKDIR /app
EXPOSE 9999
CMD ["/app/wrap"]
