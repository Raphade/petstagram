#! /bin/bash
apt-get update
apt-get install -y haproxy

# Konfiguriere HAProxy
echo "global
    log /dev/log local0
    log /dev/log local1 notice
    chroot /var/lib/haproxy
    stats socket /run/haproxy/admin.sock mode 660 level admin expose-fd listeners
    stats timeout 30s
    user haproxy
    group haproxy
    daemon

defaults
    log     global
    mode    http
    option  httplog
    option  dontlognull
    timeout connect 5s
    timeout client 5s
    timeout server 10s

frontend http-in
    bind *:8080
    default_backend backend-servers

backend backend-servers
    balance roundrobin
    option forwardfor
    server webserver1 <webserver1_internal_ip>:8000 check
    server webserver2 <webserver2_internal_ip>:8000 check
    server webserver3 <webserver3_internal_ip>:8000 check

" > /etc/haproxy/haproxy.cfg

systemctl restart haproxy