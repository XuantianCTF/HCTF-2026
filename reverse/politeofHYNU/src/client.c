/*
 * HCTF 2026 新生赛 · Reverse / C-S · Client
 *
 *   ./client.elf <host> <port>   本地 TCP，连附件里的 server.elf
 *   ./client.elf                 无参走 stdin/stdout（容器 wrap 用）
 *
 * 对端证明自己会协议之后，Client 把 flag 发给它。
 * FLAG 环境变量或 /flag 优先；都没有则发模板假 flag。
 */
#include "proto.h"

#include <arpa/inet.h>
#include <netinet/in.h>
#include <signal.h>
#include <sys/socket.h>
#include <time.h>

static int g_in = STDIN_FILENO;
static int g_out = STDOUT_FILENO;
static unsigned char g_mode = MODE_REMOTE;
static unsigned char nonce_c[NONCE_LEN];
static unsigned char nonce_s[NONCE_LEN];
static unsigned char key[KEY_LEN];

static void die(const char *why)
{
    send_pkt(g_out, CMD_ERROR, 0xff, why, (unsigned char)strlen(why));
    _exit(1);
}

static void load_flag(char *buf, size_t n)
{
    const char *env = getenv("FLAG");
    FILE *fp;

    if (env != NULL && env[0] != '\0') {
        snprintf(buf, n, "%s", env);
        return;
    }
    fp = fopen("/flag", "r");
    if (fp != NULL) {
        if (fgets(buf, (int)n, fp) != NULL) {
            buf[strcspn(buf, "\r\n")] = '\0';
            fclose(fp);
            if (buf[0] != '\0')
                return;
        } else {
            fclose(fp);
        }
    }
    snprintf(buf, n, "%s", TEMPLATE_FLAG);
}

static void do_hello(void)
{
    unsigned char payload[1 + NONCE_LEN + 4];
    unsigned char cmd, seq, len;
    unsigned char data[MAX_DATA];
    const char *helo = "HELO";
    const char *welc = "WELC";
    int i;

    payload[0] = g_mode;
    memcpy(payload + 1, nonce_c, NONCE_LEN);
    memcpy(payload + 1 + NONCE_LEN, helo, 4);
    if (send_pkt(g_out, CMD_HELLO, 0, payload, (unsigned char)sizeof(payload)) < 0)
        die("send hello");

    if (recv_pkt(g_in, &cmd, &seq, data, &len) < 0)
        die("recv welcome");
    if (cmd == CMD_ERROR)
        die("peer err");
    if (cmd != CMD_WELCOME || seq != 1 || len != 12)
        die("bad welcome");

    memcpy(nonce_s, data, NONCE_LEN);
    for (i = 0; i < NONCE_LEN; i++) {
        if (data[NONCE_LEN + i] != (unsigned char)(nonce_c[i] ^ WELCOME_XOR))
            die("bad echo");
    }
    for (i = 0; i < 4; i++) {
        if (data[8 + i] != (unsigned char)welc[i])
            die("bad welc");
    }
}

static void do_auth(void)
{
    unsigned char chal[CHAL_LEN];
    unsigned char expect[CHAL_LEN];
    unsigned char cmd, seq, len;
    unsigned char data[MAX_DATA];
    int i;

    for (i = 0; i < CHAL_LEN; i++)
        chal[i] = (unsigned char)(rand() & 0xff);

    if (send_pkt(g_out, CMD_AUTH, 2, chal, CHAL_LEN) < 0)
        die("send auth");

    if (recv_pkt(g_in, &cmd, &seq, data, &len) < 0)
        die("recv proof");
    if (cmd == CMD_ERROR)
        die("peer err");
    if (cmd != CMD_PROOF || seq != 3 || len != CHAL_LEN)
        die("bad proof");

    make_proof(expect, chal, key, nonce_c, nonce_s);
    if (memcmp(data, expect, CHAL_LEN) != 0)
        die("proof mismatch");
}

static void send_grant(void)
{
    char flag[MAX_DATA];
    load_flag(flag, sizeof(flag));
    if (send_pkt(g_out, CMD_GRANT, 4, flag, (unsigned char)strlen(flag)) < 0)
        die("send grant");
}

static int tcp_connect(const char *host, int port)
{
    int fd;
    struct sockaddr_in addr;

    fd = socket(AF_INET, SOCK_STREAM, 0);
    if (fd < 0)
        return -1;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons((unsigned short)port);
    if (inet_pton(AF_INET, host, &addr.sin_addr) != 1) {
        close(fd);
        return -1;
    }
    if (connect(fd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        close(fd);
        return -1;
    }
    return fd;
}

int main(int argc, char **argv)
{
    int sock = -1;

    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    signal(SIGPIPE, SIG_IGN);
    signal(SIGALRM, SIG_DFL);
    alarm(60);
    srand((unsigned int)time(NULL) ^ (unsigned int)getpid());
    build_key(key);

    {
        int i;
        for (i = 0; i < NONCE_LEN; i++)
            nonce_c[i] = (unsigned char)(rand() & 0xff);
    }

    if (argc >= 3) {
        g_mode = MODE_LOCAL;
        sock = tcp_connect(argv[1], atoi(argv[2]));
    } else if (argc == 2) {
        g_mode = MODE_LOCAL;
        sock = tcp_connect("127.0.0.1", atoi(argv[1]));
    } else {
        g_mode = MODE_REMOTE;
        g_in = STDIN_FILENO;
        g_out = STDOUT_FILENO;
    }

    if (g_mode == MODE_LOCAL) {
        if (sock < 0)
            return 1;
        g_in = sock;
        g_out = sock;
    }

    do_hello();
    do_auth();
    send_grant();

    if (sock >= 0)
        close(sock);
    return 0;
}
