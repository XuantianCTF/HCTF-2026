#include <stdio.h>
#include <string.h>

static const int enc[] = {
    'H', 'C', 'T', 'F', '{', 'w', '3', 'l', 'c', '0', 'm', '3', '_', '7',
    '0', '_', 'H', 'C', 'T', 'F', '_', '2', '0', '2', '6', '}',
};

int main(void)
{
    const unsigned n = sizeof(enc) / sizeof(enc[0]);
    char buf[128];

    printf("==========================================\n");
    printf("            HCTF 2026 | Sign-in\n");
    printf("==========================================\n");
    printf("Please input the flag: ");
    fflush(stdout);

    if (fgets(buf, sizeof(buf), stdin) == NULL)
        return 0;
    buf[strcspn(buf, "\r\n")] = '\0';

    if (strlen(buf) != n) {
        printf("Wrong! Keep trying :(\n");
        return 0;
    }

    for (unsigned i = 0; i < n; i++) {
        if ((unsigned char)buf[i] != (char)enc[i]) {
            printf("Wrong! Keep trying :(\n");
            return 0;
        }
    }

    printf("Correct! Welcome to HCTF 2026 :)\n");
    return 0;
}
