# web_ua_checkin deployment image (internal, do NOT publish to players)
# Single-file PHP page, pure script (libc-irrelevant), so per repo rule the
# runtime is alpine. The official php image has no apache+alpine variant,
# hence the PHP built-in web server - the same engine attachment/README.md
# tells players to run locally.
FROM php:8.3-cli-alpine

WORKDIR /var/www/html
COPY index.php .

# Built-in server is single-process by default; spawn workers for concurrency.
ENV PHP_CLI_SERVER_WORKERS=8

# Dynamic flag: the platform injects FLAG at container start (overrides the
# in-code fallback). index.php base64-encodes it into the HTML comment.
# Not set here on purpose so a missing injection is visible.
EXPOSE 80

CMD ["php", "-S", "0.0.0.0:80"]
