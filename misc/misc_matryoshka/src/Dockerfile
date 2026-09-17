# matryoshka deployment image: regenerates the polyglot attachment at
# container start with the platform-injected FLAG, then serves it over HTTP.
# Python 3 stdlib only - alpine is sufficient, no external dependencies.
FROM python:3.12-alpine

WORKDIR /app
COPY build.py entrypoint.sh ./
COPY assets ./assets/

# Dynamic flag: the platform injects FLAG at container start; build.py reads
# it and bakes the real flag into the attachment. Not set here on purpose so
# a missing injection is visible (build.py falls back to a placeholder).
EXPOSE 8080

ENTRYPOINT ["sh", "entrypoint.sh"]
