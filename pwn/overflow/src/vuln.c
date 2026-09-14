#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void win(void) {
    puts("Congratulations! Here is your flag:");
    system("cat /flag");
}

void vuln(void) {
    char buf[64];

    puts("Welcome to HCTF 2026!");
    puts("Please leave your message:");
    gets(buf);
    puts("Thanks for your message, bye~");
}

int main(void) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    vuln();
    return 0;
}
