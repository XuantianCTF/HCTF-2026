/*
 * HCTF 2026 新生赛 · Reverse / C-S · Server
 *
 *   ./server.elf [port]     默认 2333
 *
 * 只接附件 Client 的本地模式（mode='L'）。
 * 握手成功后若收到的是模板 flag 就打印；其它内容拒绝打印，
 * 避免把本程序 socat 到远端直接出真 flag。
 */
#include "proto.h"

#include <arpa/inet.h>
#include <netinet/in.h>
#include <signal.h>
#include <sys/socket.h>
#include <time.h>

static unsigned char key[KEY_LEN];

static void send_err(int fd, const char *why)
{
    send_pkt(fd, CMD_ERROR, 0xff, why, (unsigned char)strlen(why));
}

static int handle_client(int fd)
{
    unsigned char cmd, seq, len;
    unsigned char data[MAX_DATA];
    unsigned char nonce_c[NONCE_LEN];
    unsigned char nonce_s[NONCE_LEN];
    unsigned char chal[CHAL_LEN];
    unsigned char proof[CHAL_LEN];
    unsigned char welcome[12];
    unsigned char mode;
    char grant[MAX_DATA + 1];
    const char *helo = "HELO";
    const char *welc = "WELC";
    int i;

    if (recv_pkt(fd, &cmd, &seq, data, &len) < 0) {
        send_err(fd, "bad pkt");
        return -1;
    }
    if (cmd != CMD_HELLO || seq != 0 || len != 9) {
        send_err(fd, "bad hello");
        return -1;
    }
    mode = data[0];
    if (mode != MODE_LOCAL) {
        send_err(fd, "local only");
        return -1;
    }
    memcpy(nonce_c, data + 1, NONCE_LEN);
    if (memcmp(data + 1 + NONCE_LEN, helo, 4) != 0) {
        send_err(fd, "bad helo");
        return -1;
    }

    for (i = 0; i < NONCE_LEN; i++)
        nonce_s[i] = (unsigned char)(rand() & 0xff);
    memcpy(welcome, nonce_s, NONCE_LEN);
    for (i = 0; i < NONCE_LEN; i++)
        welcome[NONCE_LEN + i] = (unsigned char)(nonce_c[i] ^ WELCOME_XOR);
    memcpy(welcome + 8, welc, 4);
    if (send_pkt(fd, CMD_WELCOME, 1, welcome, 12) < 0)
        return -1;

    if (recv_pkt(fd, &cmd, &seq, data, &len) < 0) {
        send_err(fd, "bad pkt");
        return -1;
    }
    if (cmd != CMD_AUTH || seq != 2 || len != CHAL_LEN) {
        send_err(fd, "bad auth");
        return -1;
    }
    memcpy(chal, data, CHAL_LEN);
    make_proof(proof, chal, key, nonce_c, nonce_s);
    if (send_pkt(fd, CMD_PROOF, 3, proof, CHAL_LEN) < 0)
        return -1;

    if (recv_pkt(fd, &cmd, &seq, data, &len) < 0) {
        send_err(fd, "bad pkt");
        return -1;
    }
    if (cmd != CMD_GRANT || seq != 4 || len == 0) {
        send_err(fd, "bad grant");
        return -1;
    }
    memcpy(grant, data, len);
    grant[len] = '\0';

    if (strcmp(grant, TEMPLATE_FLAG) != 0) {
        send_err(fd, "not template");
        fprintf(stderr, "[server] refuse non-template grant\n");
        return -1;
    }
    printf("%s\n", grant);
    fflush(stdout);
    return 0;
}

int main(int argc, char **argv)
{
    int srv, opt = 1;
    int port = 2333;
    struct sockaddr_in addr;

    if (argc >= 2)
        port = atoi(argv[1]);

    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    signal(SIGCHLD, SIG_IGN);
    signal(SIGPIPE, SIG_IGN);
    srand((unsigned int)time(NULL) ^ (unsigned int)getpid());
    build_key(key);

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
    if (listen(srv, 16) < 0)
        return 1;

    fprintf(stderr, "[server] listen 0.0.0.0:%d\n", port);

    for (;;) {
        int cli = accept(srv, NULL, NULL);
        pid_t pid;
        if (cli < 0)
            continue;
        pid = fork();
        if (pid == 0) {
            close(srv);
            alarm(30);
            handle_client(cli);
            close(cli);
            _exit(0);
        }
        close(cli);
        (void)pid;
    }
}
