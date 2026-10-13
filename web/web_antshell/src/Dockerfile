# web_antshell deployment image (internal, do NOT publish to players)
# 纯 PHP 单页站点（与 libc 无关），按仓库规范用 alpine 系运行时；
# 官方 php 镜像无 apache+alpine 变体，故用 PHP 内置服务器（与选手本地复现同引擎）。
FROM php:8.3-cli-alpine

WORKDIR /var/www/html
COPY html/ .

# 站点备份包（源码泄漏入口）：构建期打包，与部署文件一一对应
#（官方 php:cli-alpine 镜像不带 zip 扩展，装 zip 命令最直接，体积可忽略）
RUN apk add --no-cache zip \
    && mkdir -p backup \
    && zip -q backup/antcloud_backup.zip index.php ant.php config.php robots.txt

# 内置服务器默认单进程，起 workers 提并发
ENV PHP_CLI_SERVER_WORKERS=8

# 动态 FLAG：平台在容器启动时注入 FLAG（entrypoint 写入 /flag，未注入则回退默认值）
EXPOSE 80

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
