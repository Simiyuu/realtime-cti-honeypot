FROM cowrie/cowrie:latest

USER root

RUN echo '[honeypot]' > /cowrie/cowrie-git/etc/cowrie.cfg && \
    echo 'hostname = mku-webserver-01' >> /cowrie/cowrie-git/etc/cowrie.cfg && \
    echo '' >> /cowrie/cowrie-git/etc/cowrie.cfg && \
    echo '[ssh]' >> /cowrie/cowrie-git/etc/cowrie.cfg && \
    echo 'enabled = true' >> /cowrie/cowrie-git/etc/cowrie.cfg && \
    echo 'listen_endpoints = tcp:2222:interface=0.0.0.0' >> /cowrie/cowrie-git/etc/cowrie.cfg && \
    echo 'version = SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.6' >> /cowrie/cowrie-git/etc/cowrie.cfg

USER cowrie
