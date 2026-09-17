FROM golang:1.21-bookworm AS builder

WORKDIR /build
COPY main.go .
RUN go mod init ezgo \
    && CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -trimpath -o ezgo .

FROM alpine:3.19

WORKDIR /app
COPY --from=builder /build/ezgo /app/ezgo
RUN chmod +x /app/ezgo

CMD ["/app/ezgo"]
