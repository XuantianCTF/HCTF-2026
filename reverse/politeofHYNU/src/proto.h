#ifndef PROTO_H
#define PROTO_H

/*
 * HCTF 2026 新生赛 · C/S 自定义协议
 * 附件里的 client.elf / server.elf 共用这份帧格式。
 */

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MAGIC0 'P'
#define MAGIC1 'x'
#define MAGIC2 'T'
#define MAGIC3 'L'

#define CMD_HELLO   0xA1
#define CMD_WELCOME 0xA2
#define CMD_AUTH    0xA3
#define CMD_PROOF   0xA4
#define CMD_GRANT   0xA5
#define CMD_ERROR   0xEE

#define MODE_LOCAL  0x4C /* 'L' 附件互聊 */
#define MODE_REMOTE 0x52 /* 'R' 容器 stdio */

#define MAX_DATA    128
#define HDR_LEN     7    /* magic4 + cmd + seq + len */
#define KEY_LEN     8
#define NONCE_LEN   4
#define CHAL_LEN    8
#define WELCOME_XOR 0x5A

/* 静态附件互聊拿到的模板 / 假 flag，交平台不得分 */
#define TEMPLATE_FLAG "HCTF{1bab71b8-117f-4dea-a047-340b72101d7b}"

int write_all(int fd, const void *buf, int n);
int read_all(int fd, void *buf, int n);
int send_pkt(int fd, unsigned char cmd, unsigned char seq,
             const void *data, unsigned char len);
int recv_pkt(int fd, unsigned char *cmd, unsigned char *seq,
             unsigned char *data, unsigned char *len);
void build_key(unsigned char *key);
void make_proof(unsigned char *out, const unsigned char *chal,
                const unsigned char *key,
                const unsigned char *nonce_c,
                const unsigned char *nonce_s);

#endif
