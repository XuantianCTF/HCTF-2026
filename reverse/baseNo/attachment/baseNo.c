#include <stdio.h>
#include <string.h>
#include <stdint.h>

static const char *TABLE =
    "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm0123456789+/";

static const unsigned char KEY[4] = {'H', 'C', 'T', 'F'};

static const unsigned char CIPHER[] = {
    0x04, 0x17, 0x12, 0x1e, 0x03, 0x25, 0x2e, 0x36, 0x3a, 0x19, 0x17, 0x76,
    0x0c, 0x16, 0x65, 0x3f, 0x06, 0x33, 0x1f, 0x2b, 0x0c, 0x72, 0x6c, 0x74,
    0x0e, 0x1a, 0x6c, 0x75, 0x0e, 0x16, 0x04, 0x2a, 0x0c, 0x70, 0x64, 0x7b,
};

static size_t custom_b64(const unsigned char *in, size_t n, char *out)
{
    size_t o = 0;
    for (size_t i = 0; i < n; i += 3) {
        size_t left = n - i;
        uint32_t v = (uint32_t)in[i] << 16;
        if (left > 1) v |= (uint32_t)in[i + 1] << 8;
        if (left > 2) v |= (uint32_t)in[i + 2];

        out[o++] = TABLE[(v >> 18) & 0x3f];
        out[o++] = TABLE[(v >> 12) & 0x3f];
        out[o++] = (left > 1) ? TABLE[(v >> 6) & 0x3f] : '=';
        out[o++] = (left > 2) ? TABLE[v & 0x3f] : '=';
    }
    out[o] = '\0';
    return o;
}

static int check(const char *flag)
{
    char enc[512];
    size_t n = custom_b64((const unsigned char *)flag, strlen(flag), enc);

    if (n != sizeof(CIPHER))
        return 0;

    for (size_t i = 0; i < n; i++) {
        if ((unsigned char)(enc[i] ^ KEY[i % 4]) != CIPHER[i])
            return 0;
    }
    return 1;
}

int main(void)
{
    char buf[256];
    memset(buf, 0, sizeof(buf));

    printf("==========================================\n");
    printf("            HCTF 2026 | baseNo\n");
    printf("==========================================\n");
    printf("Please input the flag: ");
    fflush(stdout);

    if (fgets(buf, sizeof(buf), stdin) == NULL)
        return 0;

    buf[strcspn(buf, "\r\n")] = '\0';

    if (check(buf))
        printf("Correct! You cracked the custom table :)\n");
    else
        printf("Wrong! Keep trying :(\n");

    return 0;
}
