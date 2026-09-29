# AGENTS.md

HCTF 2026 challenge archive. There is **no root build system, package manager, lint, or test suite** — verification is per-challenge Docker builds. The GitHub Actions workflows in `.github/workflows/` are the source of truth; `README.md` is largely an aspirational template (its example names like `web_ez_sqli` do not exist).

## Layout (only these are recognized by CI)

```
<category>/<challenge>/
├── README.md                # required — CI errors if missing
├── src/Dockerfile           # private deploy build; required for web/pwn/crypto/misc,
│                            # optional for reverse/mobile (offline challenges)
├── attachment/Dockerfile    # public player build; optional (warns if absent)
└── writeup/                 # private exp + notes
```

- Categories: `web`, `pwn`, `crypto`, `misc`, `reverse`, `mobile`. `crypto/` is currently empty (`.gitkeep`).
- A path counts as a challenge only when it is `$1/$2/...` with `$1` one of the categories (`pr-check.yml`).
- Older challenges (`web/headers`, `web/request`) put the deploy `Dockerfile` at the challenge root instead of `src/`. Do not "fix" them; new challenges use the `src/` + `attachment/` split.

## Verify locally (no CI command exists for this)

```bash
# deployment image  (expects FLAG env at runtime for dynamic flag)
docker build -t <name> <category>/<name>/src && docker run --rm -p 9999:9999 -e FLAG='HCTF{test}' <name>

# reproduce exactly what the attachment CI extracts
docker build --target builder -t tmp <cat>/<name>/attachment
id=$(docker create tmp); docker cp "$id:/build/." out/; docker rm "$id"

# Android APK (outputs /build/ezjdk.apk)
docker build --target builder -t mobile-ezjdk ./mobile/ezjdk/attachment
```

## `attachment/Dockerfile` rules (enforced by `attachment.yml`)

- Must be multi-stage with the compile stage named exactly `builder` (`FROM ... AS builder`).
- Compile output **must** land in `/build`. CI scans `/build` at maxdepth 1 for an executable `ELF*` or `PE32*`, else a `*.apk`. If none is found the build fails.
- pwn: copy runtime `libc.so.6` + dynamic loader into `/build/libc/`; CI then publishes `<name>.zip` instead of a bare binary.
- Build for **linux/amd64 + glibc** (`ubuntu:22.04` etc.); never rely on the host toolchain (devs are on macOS/ARM).
- `attachment/` is public — only demo flags. Dynamic flags come from the `FLAG` env var at runtime.

## Derived names (do not hardcode)

- Slug = challenge dir path lowercased, non-`[a-z0-9]` → `-`. `web/web_headerauth` → `web-web_headerauth`.
- Deploy images (any `Dockerfile` **not** under `attachment/`) are pushed to `ghcr.io/<owner>/hctf-2026/<slug>` on push to `main`. Note `src/Dockerfile` produces slug `<cat>-<name>-src` because the dirname includes `src`; root-`Dockerfile` challenges like `web/request` produce `web-request`.
- Attachment binaries attach to a single release tagged `attachments` (assets overwritten). To republish without code changes, use `workflow_dispatch` or touch a file under `attachment/` (see commit `ci(attachment): trigger baseNo republish`).
- CI triggers incrementally on `git diff` of the base commit; a force push causes a full rebuild.

## Conventions / gotchas

- Dynamic flag: the ret2shell platform injects `FLAG` into the container; `src/` should read it (`pr-check.yml` warns if `src/` never mentions `FLAG`).
- Flag prefix is `HCTF` (`HCTF{...}`); checker scripts on ret2shell must set `PREFIX = "HCTF"` (see `FAQ.md`).
- Contribution flow: fork → branch named after the challenge → PR to `main`. Commit style: `[<category>]: <name>` for new challenges, plus `ci(scope):` / `fix(scope):`. Most docs, READMEs, and PR text are Chinese.
- Android challenges target minSdk 24 / targetSdk 34; CI installs `platforms;android-34` + `build-tools;34.0.0` and builds a debug APK via Gradle wrapper.
- Platform-specific creation steps live in `FAQ.md` (ret2shell), not here.
