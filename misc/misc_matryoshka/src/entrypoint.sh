#!/bin/sh
# Regenerate the attachment with the (platform-injected) FLAG, then serve it.
set -eu
python3 build.py
exec python3 -m http.server 8080 --bind 0.0.0.0 --directory dist
