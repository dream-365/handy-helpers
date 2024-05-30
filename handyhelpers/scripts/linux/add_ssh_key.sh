#!/bin/bash
# bash <(curl -fsSL https://example.com/path/to/add_ssh_key.sh) https://example.com/path/to/your/public_key.pub

# 第一个参数是公钥文件的URL
PUB_KEY_URL=$1

# 临时存储位置
TEMP_PUB_KEY_PATH="/tmp/ssh_public_key.pub"

# 检查URL变量是否给出
if [ -z "$PUB_KEY_URL" ]; then
    echo "Usage: $0 <public-key-url>"
    exit 1
fi

# 下载公钥文件
curl -fsSL -o "$TEMP_PUB_KEY_PATH" "$PUB_KEY_URL" || {
    echo "Failed to download the public key file from URL: $PUB_KEY_URL"
    exit 1
}

# 创建 ~/.ssh 目录（如果不存在）
mkdir -p "$HOME/.ssh"
chmod 700 "$HOME/.ssh"

# 将下载的公钥添加到 ~/.ssh/authorized_keys
cat "$TEMP_PUB_KEY_PATH" >> "$HOME/.ssh/authorized_keys"
chmod 600 "$HOME/.ssh/authorized_keys"

# 清理临时文件
rm -f "$TEMP_PUB_KEY_PATH"

echo "The public key has been added to your authorized_keys."