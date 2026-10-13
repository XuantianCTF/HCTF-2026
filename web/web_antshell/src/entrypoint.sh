#!/bin/sh
# 动态 FLAG：平台注入 FLAG 时写入 /flag；未注入时回退默认值（保持 hctf{} 格式，静态部署可用）
if [ -z "$FLAG" ]; then
    FLAG='hctf{AntSword_0n1y}'
fi
printf '%s' "$FLAG" > /flag
chmod 0644 /flag

exec php -S 0.0.0.0:80 -t /var/www/html
