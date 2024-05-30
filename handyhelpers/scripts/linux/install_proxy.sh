#!/bin/bash
# bash <(curl -fsSL https://example.com/path/to/install_proxy.sh) your_password

# 第一个参数是password
PASSWORD=$1

# 检查第一个参数是password变量是否给出
if [ -z "$PASSWORD" ]; then
    echo "Usage: $0 <password>"
    exit 1
fi

docker run -e PASSWORD="$PASSWORD" \
-e METHOD="aes-256-cfb" \
-p8000:8388 -p8000:8388/udp \
-d shadowsocks/shadowsocks-libev

echo "The proxy service has been installled."