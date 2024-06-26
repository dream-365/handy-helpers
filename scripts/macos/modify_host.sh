#!/bin/bash
# 下载文件， 保存至：/opt/custom/modify_host.sh
# chmod +x /opt/custom/modify_host.sh
# vim ~/.zshrc
# alias modify_host="/opt/custom/modify_host.sh"
# source ~/.zshrc


# 函数：添加 hosts 条目
add_host() {
    # 检查是否已存在相同的主机名，如果存在则删除
    remove_host "$2"
    echo "$1 $2" | sudo tee -a /etc/hosts >/dev/null
}

# 函数：删除 hosts 条目
remove_host() {
    sudo sed -i '' "/$1/d" /etc/hosts
}

# 主程序

# 检查参数数量
if [ $# -lt 2 ]; then
    echo "Usage: $0 [add|remove] [hostname] [IP]"
    exit 1
fi

action="$1"
hostname="$2"
ip="$3"

# 根据操作调用相应函数
case "$action" in
    "add")
        add_host "$ip" "$hostname"
        echo "Added $hostname to hosts file."
        ;;
    "remove")
        remove_host "$hostname"
        echo "Removed $hostname from hosts file."
        ;;
    *)
        echo "Invalid action. Please use 'add' or 'remove'."
        exit 1
        ;;
esac

exit 0