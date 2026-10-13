# web_antshell deployment image (internal, do NOT publish to players)
# 单文件 PHP 页（与 libc 无关），按仓库规范用 alpine 系运行时；
# 官方 php 镜像无 apache+alpine 变体，故用 PHP 内置服务器（与选手本地复现同引擎）。
FROM php:8.3-cli-alpine

WORKDIR /var/www/html
COPY html/ .

# 内置服务器默认单进程，起 workers 提并发
ENV PHP_CLI_SERVER_WORKERS=8

# 动态 FLAG：平台在容器启动时注入 FLAG（entrypoint 写入 /flag，未注入则回退默认值）
EXPOSE 80

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
