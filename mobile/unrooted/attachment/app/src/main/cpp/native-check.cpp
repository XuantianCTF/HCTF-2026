#include <jni.h>

#include <arpa/inet.h>
#include <dirent.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/system_properties.h>
#include <unistd.h>

#include <cstdio>
#include <cstring>
#include <fstream>
#include <string>

namespace {

const char *kMask = "unrooted";
const char *kSecret = "PS0mKRQaVTsHXkIbMBpVOxMcQwtbKw8RQBotWwEQF1RECg8=";

bool FileExists(const char *path) {
    struct stat st;
    return stat(path, &st) == 0;
}

std::string GetProp(const char *key) {
    char value[PROP_VALUE_MAX] = {0};
    __system_property_get(key, value);
    return std::string(value);
}

bool IsRooted() {
    const char *paths[] = {
        "/system/bin/su",
        "/system/xbin/su",
        "/sbin/su",
        "/su/bin/su",
        "/system/sd/xbin/su",
        "/system/bin/failsafe/su",
        "/data/local/su",
        "/data/local/bin/su",
        "/data/local/xbin/su",
        "/debug_ramdisk/su",
    };
    for (const char *path : paths) {
        if (FileExists(path)) {
            return true;
        }
    }

    if (FileExists("/sbin/.magisk") || FileExists("/data/adb/magisk") ||
        FileExists("/data/adb/ksu")) {
        return true;
    }

    if (GetProp("ro.build.tags").find("test-keys") != std::string::npos) {
        return true;
    }
    if (GetProp("ro.debuggable") == "1" || GetProp("ro.secure") == "0") {
        return true;
    }
    return false;
}

bool FileContains(const char *path, const char *needle) {
    std::ifstream stream(path);
    if (!stream.is_open()) {
        return false;
    }
    std::string line;
    while (std::getline(stream, line)) {
        if (line.find(needle) != std::string::npos) {
            return true;
        }
    }
    return false;
}

bool ThreadsContain(const char *needle) {
    DIR *dir = opendir("/proc/self/task");
    if (dir == nullptr) {
        return false;
    }
    bool found = false;
    struct dirent *entry;
    while ((entry = readdir(dir)) != nullptr) {
        if (entry->d_name[0] == '.') {
            continue;
        }
        std::string comm = std::string("/proc/self/task/") + entry->d_name + "/comm";
        std::ifstream stream(comm);
        std::string name;
        if (std::getline(stream, name) && name.find(needle) != std::string::npos) {
            found = true;
            break;
        }
    }
    closedir(dir);
    return found;
}

bool IsFridaDetected() {
    if (FileContains("/proc/self/maps", "frida") ||
        FileContains("/proc/self/maps", "gum-js-loop") ||
        FileContains("/proc/self/maps", "gadget") ||
        FileContains("/proc/self/maps", "linjector")) {
        return true;
    }

    if (ThreadsContain("gum-js-loop") || ThreadsContain("gmain") ||
        ThreadsContain("frida")) {
        return true;
    }

    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock >= 0) {
        struct sockaddr_in addr;
        memset(&addr, 0, sizeof(addr));
        addr.sin_family = AF_INET;
        addr.sin_port = htons(27042);
        addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
        if (connect(sock, reinterpret_cast<struct sockaddr *>(&addr),
                    sizeof(addr)) == 0) {
            close(sock);
            return true;
        }
        close(sock);
    }
    return false;
}

bool IsDebuggerAttached() {
    std::ifstream status("/proc/self/status");
    if (!status.is_open()) {
        return false;
    }
    std::string line;
    while (std::getline(status, line)) {
        if (line.rfind("TracerPid:", 0) == 0) {
            int pid = 0;
            if (sscanf(line.c_str(), "TracerPid:%d", &pid) == 1 && pid > 0) {
                return true;
            }
            break;
        }
    }
    return false;
}

int CheckEnvironment() {
    int status = 0;
    if (IsRooted()) {
        status |= 0x1;
    }
    if (IsFridaDetected()) {
        status |= 0x2;
    }
    if (IsDebuggerAttached()) {
        status |= 0x4;
    }
    return status;
}

std::string Base64Encode(const std::string &input) {
    static const char kTable[] =
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    std::string output;
    int value = 0;
    int bits = -6;
    for (unsigned char c : input) {
        value = (value << 8) + c;
        bits += 8;
        while (bits >= 0) {
            output.push_back(kTable[(value >> bits) & 0x3F]);
            bits -= 6;
        }
    }
    if (bits > -6) {
        output.push_back(kTable[((value << 8) >> (bits + 8)) & 0x3F]);
    }
    while (output.size() % 4 != 0) {
        output.push_back('=');
    }
    return output;
}

}  // namespace

extern "C" JNIEXPORT jint JNICALL
Java_com_example_unrooted_NativeCheck_checkEnvironment(JNIEnv *env, jobject thiz,
                                                       jobject context) {
    (void) env;
    (void) thiz;
    (void) context;
    return CheckEnvironment();
}

extern "C" JNIEXPORT jboolean JNICALL
Java_com_example_unrooted_NativeCheck_verifyFlag(JNIEnv *env, jobject thiz,
                                                 jstring input) {
    (void) thiz;
    if (input == nullptr) {
        return JNI_FALSE;
    }

    const char *raw = env->GetStringUTFChars(input, nullptr);
    if (raw == nullptr) {
        return JNI_FALSE;
    }
    std::string text(raw);
    env->ReleaseStringUTFChars(input, raw);

    std::string mask(kMask);
    std::string encoded(text.size(), '\0');
    for (size_t i = 0; i < text.size(); ++i) {
        encoded[i] = static_cast<char>(text[i] ^ mask[i % mask.size()]);
    }

    return Base64Encode(encoded) == kSecret ? JNI_TRUE : JNI_FALSE;
}
