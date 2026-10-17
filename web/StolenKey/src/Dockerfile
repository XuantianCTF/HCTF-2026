# StolenKey deployment image (internal, do NOT publish to players)
#
# The weakness is intentional: /etc/skel is writable by the low-privileged
# guest account, while cron recreates the admin account from that skeleton
# every minute and runs its login shell as admin.
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    cron \
    sudo \
    passwd \
    openssh-server \
    && rm -rf /var/lib/apt/lists/*

# SSH: allow password login, forbid root login, generate host keys at build time.
RUN mkdir -p /var/run/sshd && \
    sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config && \
    echo 'UseDNS no' >> /etc/ssh/sshd_config && \
    ssh-keygen -A

# Low-privileged entry account.
RUN useradd -m -s /bin/bash guest && \
    echo "guest:guest" | chpasswd

# Intentional vulnerability: guest owns the skeleton used for new users.
RUN chown -R guest:guest /etc/skel

# Every minute the admin account is recreated from /etc/skel, receives the
# flag, and then starts an interactive login shell (which sources .bashrc).
RUN cat > /etc/cron.d/admin-job << 'EOF'
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
*/1 * * * * root userdel -r admin 2>/dev/null; useradd -m -s /bin/bash admin && cp /root/flag.txt /home/admin/.flag && chown admin:admin /home/admin/.flag && chmod 400 /home/admin/.flag && su -l admin -c 'bash --login -i -c exit'
EOF
RUN chmod 0644 /etc/cron.d/admin-job

RUN echo 'admin ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/admin && \
    chmod 440 /etc/sudoers.d/admin

RUN cat > /etc/motd << 'EOF'

===========================================
  CTF Challenge: StolenKey
===========================================
  User    : guest / guest
  Goal    : Read /root/flag.txt
  Hint    : Something happens every minute
===========================================

EOF

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 22

CMD ["/entrypoint.sh"]
