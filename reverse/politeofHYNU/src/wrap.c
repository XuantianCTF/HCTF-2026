/* 极简 inetd：准备 FLAG，监听 9999，每个连接 fork 一份 client.elf（stdio） */
#include <arpa/inet.h>
#include <netinet/in.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

static void ensure_flag(void)
{
    const char *env = getenv("FLAG");
    char buf[80];
    unsigned char u[16];
    FILE *fp;

    if (env != NULL && env[0] != '\0')
        return;

    fp = fopen("/flag", "r");
    if (fp != NULL) {
        if (fgets(buf, (int)sizeof(buf), fp) != NULL) {
            buf[strcspn(buf, "\r\n")] = '\0';
            if (buf[0] != '\0') {
                fclose(fp);
                setenv("FLAG", buf, 1);
                return;
            }
        }
        fclose(fp);
    }

    fp = fopen("/dev/urandom", "rb");
    if (fp == NULL || fread(u, 1, 16, fp) != 16) {
        if (fp != NULL)
            fclose(fp);
        _exit(1);
    }
    fclose(fp);
    snprintf(buf, sizeof(buf),
             "HCTF{%02x%02x%02x%02x-%02x%02x-%02x%02x-%02x%02x-%02x%02x%02x%02x%02x%02x}",
             u[0], u[1], u[2], u[3], u[4], u[5], u[6], u[7], u[8], u[9],
             u[10], u[11], u[12], u[13], u[14], u[15]);
    setenv("FLAG", buf, 1);
}

int main(void)
{
    int srv, opt = 1;
    struct sockaddr_in addr;
    const char *port_s = getenv("PORT");
    int port = port_s && port_s[0] ? atoi(port_s) : 9999;

    ensure_flag();
    signal(SIGCHLD, SIG_IGN);
    signal(SIGPIPE, SIG_IGN);

    srv = socket(AF_INET, SOCK_STREAM, 0);
    if (srv < 0)
        return 1;
    setsockopt(srv, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(INADDR_ANY);
    addr.sin_port = htons((unsigned short)port);
    if (bind(srv, (struct sockaddr *)&addr, sizeof(addr)) < 0)
        return 1;
    if (listen(srv, 32) < 0)
        return 1;

    for (;;) {
        int cli = accept(srv, NULL, NULL);
        pid_t pid;
        if (cli < 0)
            continue;
        pid = fork();
        if (pid == 0) {
            close(srv);
            dup2(cli, STDIN_FILENO);
            dup2(cli, STDOUT_FILENO);
            close(cli);
            execl("/app/client.elf", "client.elf", (char *)NULL);
            _exit(1);
        }
        close(cli);
        (void)pid;
    }
}
