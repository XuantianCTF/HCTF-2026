# 单容器部署：PHP 内置服务器直出静态题目站点（平台一题一容器）
FROM php:8.3-cli-alpine

ENV PHP_CLI_SERVER_WORKERS=8
WORKDIR /app
COPY . .
EXPOSE 80
CMD ["php", "-S", "0.0.0.0:80", "-t", "/app"]
