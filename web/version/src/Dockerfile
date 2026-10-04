# web_version deployment image (internal, do NOT publish to players)
#
# The app is shipped as a real Subversion working copy: the metadata directory
# (.svn) is left in place on purpose (see server.js -> /.svn mount). The
# svnbuilder stage creates a genuine wc.db + pristine store from the sources so
# the leak is authentic rather than hand-crafted.
FROM node:20-alpine AS svnbuilder
RUN apk add --no-cache subversion
WORKDIR /build
COPY app/ /build/app/
RUN svnadmin create /build/repo \
 && svn import /build/app file:///build/repo/trunk -m "release panel 1.4.2" >/dev/null \
 && svn checkout file:///build/repo/trunk /build/wc >/dev/null

FROM node:20-alpine
WORKDIR /app
COPY --from=svnbuilder /build/wc/ /app/
RUN npm install --omit=dev --no-audit --no-fund

ENV NODE_ENV=production

# Dynamic flag: the platform injects FLAG at container start; the admin backup
# endpoint spawns a shell, so the flag must only ever live in the environment.
EXPOSE 3000

CMD ["node", "server.js"]
