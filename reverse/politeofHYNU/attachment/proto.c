#include "proto.h"

int write_all(int fd, const void *buf, int n)
{
    const unsigned char *p = (const unsigned char *)buf;
    int off = 0;
    while (off < n) {
        int w = (int)write(fd, p + off, (size_t)(n - off));
        if (w <= 0)
            return -1;
        off += w;
    }
    return 0;
}

int read_all(int fd, void *buf, int n)
{
    unsigned char *p = (unsigned char *)buf;
    int off = 0;
    while (off < n) {
        int r = (int)read(fd, p + off, (size_t)(n - off));
        if (r <= 0)
            return -1;
        off += r;
    }
    return 0;
}

static unsigned char pkt_cksum(const unsigned char *buf, int n)
{
    unsigned char c = 0;
    int i;
    for (i = 0; i < n; i++)
        c ^= buf[i];
    return c;
}

int send_pkt(int fd, unsigned char cmd, unsigned char seq,
             const void *data, unsigned char len)
{
    unsigned char buf[HDR_LEN + MAX_DATA + 1];
    if (len > MAX_DATA)
        return -1;
    buf[0] = MAGIC0;
    buf[1] = MAGIC1;
    buf[2] = MAGIC2;
    buf[3] = MAGIC3;
    buf[4] = cmd;
    buf[5] = seq;
    buf[6] = len;
    if (len != 0)
        memcpy(buf + HDR_LEN, data, len);
    buf[HDR_LEN + len] = pkt_cksum(buf, HDR_LEN + len);
    return write_all(fd, buf, HDR_LEN + len + 1);
}

int recv_pkt(int fd, unsigned char *cmd, unsigned char *seq,
             unsigned char *data, unsigned char *len)
{
    unsigned char hdr[HDR_LEN];
    unsigned char body[MAX_DATA];
    unsigned char ck, expect;
    if (read_all(fd, hdr, HDR_LEN) < 0)
        return -1;
    if (hdr[0] != MAGIC0 || hdr[1] != MAGIC1 ||
        hdr[2] != MAGIC2 || hdr[3] != MAGIC3)
        return -2;
    *cmd = hdr[4];
    *seq = hdr[5];
    *len = hdr[6];
    if (*len > MAX_DATA)
        return -3;
    if (*len != 0 && read_all(fd, body, *len) < 0)
        return -1;
    if (read_all(fd, &ck, 1) < 0)
        return -1;
    expect = pkt_cksum(hdr, HDR_LEN);
    if (*len != 0)
        expect ^= pkt_cksum(body, *len);
    if (ck != expect)
        return -4;
    if (*len != 0)
        memcpy(data, body, *len);
    return 0;
}

static unsigned char hex_nibble(char c)
{
    if (c >= '0' && c <= '9')
        return (unsigned char)(c - '0');
    if (c >= 'a' && c <= 'f')
        return (unsigned char)(c - 'a' + 10);
    if (c >= 'A' && c <= 'F')
        return (unsigned char)(c - 'A' + 10);
    return 0;
}

void build_key(unsigned char *key)
{
    const char *p = TEMPLATE_FLAG + 5; /* skip HCTF{ */
    int i = 0;
    memset(key, 0, KEY_LEN);
    while (i < KEY_LEN && *p != '\0' && *p != '}') {
        if (*p == '-') {
            p++;
            continue;
        }
        if (p[0] == '\0' || p[1] == '\0')
            break;
        key[i] = (unsigned char)((hex_nibble(p[0]) << 4) | hex_nibble(p[1]));
        p += 2;
        i++;
    }
}

void make_proof(unsigned char *out, const unsigned char *chal,
                const unsigned char *key,
                const unsigned char *nonce_c,
                const unsigned char *nonce_s)
{
    unsigned char mix[CHAL_LEN];
    int i;
    memcpy(mix, nonce_c, NONCE_LEN);
    memcpy(mix + NONCE_LEN, nonce_s, NONCE_LEN);
    for (i = 0; i < CHAL_LEN; i++)
        out[i] = (unsigned char)(chal[i] ^ key[i] ^ mix[i]);
}
