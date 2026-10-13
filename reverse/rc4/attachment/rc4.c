#include <stdio.h>
#include <string.h>

static const unsigned char key[] = "hctf2026_standard_rc4";
static const unsigned char ciphertext[] = {
    0x62, 0x4a, 0xc1, 0xdd, 0x81, 0x96, 0x0f, 0x32, 0xa2, 0x24,
    0xec, 0xbd, 0xfa, 0x72, 0xaf, 0xfa, 0xce, 0xf7, 0xec, 0x8e,
    0x08, 0x37, 0x49, 0xa5, 0x47, 0xb3, 0x86, 0x9e,
};

static void rc4(const unsigned char *input, unsigned char *output, size_t length)
{
    unsigned char state[256];
    size_t key_length = sizeof(key) - 1;
    unsigned int j = 0;

    for (unsigned int i = 0; i < 256; i++)
        state[i] = (unsigned char)i;

    for (unsigned int i = 0; i < 256; i++) {
        j = (j + state[i] + key[i % key_length]) & 0xff;
        unsigned char temp = state[i];
        state[i] = state[j];
        state[j] = temp;
    }

    unsigned int i = 0;
    j = 0;
    for (size_t n = 0; n < length; n++) {
        i = (i + 1) & 0xff;
        j = (j + state[i]) & 0xff;
        unsigned char temp = state[i];
        state[i] = state[j];
        state[j] = temp;
        unsigned char stream = state[(state[i] + state[j]) & 0xff];
        output[n] = input[n] ^ stream;
    }
}

int main(void)
{
    char input[128];
    unsigned char encrypted[sizeof(ciphertext)];

    printf("Input flag: ");
    fflush(stdout);

    if (fgets(input, sizeof(input), stdin) == NULL)
        return 0;
    input[strcspn(input, "\r\n")] = '\0';

    if (strlen(input) != sizeof(ciphertext)) {
        puts("Wrong.");
        return 0;
    }

    rc4((const unsigned char *)input, encrypted, sizeof(ciphertext));
    if (memcmp(encrypted, ciphertext, sizeof(ciphertext)) == 0)
        puts("Correct!");
    else
        puts("Wrong.");

    return 0;
}
