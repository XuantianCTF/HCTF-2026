# web_ua_checkin deployment image (internal, do NOT publish to players)
# Single-file PHP page, no extensions beyond the stock apache build.
FROM php:8.3-apache

COPY index.php /var/www/html/

# Dynamic flag: the platform injects FLAG at container start (overrides the
# in-code fallback). index.php base64-encodes it into the HTML comment.
# Not set here on purpose so a missing injection is visible.
EXPOSE 80
