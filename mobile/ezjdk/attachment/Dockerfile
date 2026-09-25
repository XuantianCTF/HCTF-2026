FROM ubuntu:22.04 AS builder

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        openjdk-17-jdk \
        unzip \
        wget \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

ENV ANDROID_SDK_ROOT=/opt/android-sdk
ENV ANDROID_HOME=/opt/android-sdk
ENV PATH=${ANDROID_SDK_ROOT}/cmdline-tools/latest/bin:${ANDROID_SDK_ROOT}/platform-tools:${PATH}

RUN mkdir -p "${ANDROID_SDK_ROOT}/cmdline-tools" \
    && wget -q https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip -O /tmp/cmdline-tools.zip \
    && unzip -q /tmp/cmdline-tools.zip -d /tmp/cmdline-tools \
    && mv /tmp/cmdline-tools/cmdline-tools "${ANDROID_SDK_ROOT}/cmdline-tools/latest" \
    && rm -rf /tmp/cmdline-tools /tmp/cmdline-tools.zip

RUN yes | sdkmanager --licenses > /dev/null \
    && sdkmanager --install "platforms;android-34" "build-tools;34.0.0" > /dev/null

WORKDIR /build
COPY . .

RUN chmod +x gradlew \
    && ./gradlew --no-daemon :app:assembleDebug \
    && cp app/build/outputs/apk/debug/app-debug.apk /build/ezjdk.apk

FROM alpine:3.19 AS runtime

WORKDIR /app
COPY --from=builder /build/ezjdk.apk /app/ezjdk.apk

CMD ["sh", "-c", "echo 'ezjdk is an offline Android reverse challenge.'; echo 'Analyze /app/ezjdk.apk to recover the flag.'"]
