# CentOS 8 \ AliLinux3

sudo dnf config-manager --add-repo=https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
sudo dnf -y install dnf-plugin-releasever-adapter --repo alinux3-plus
sudo dnf -y install docker-ce --nobest
sudo systemctl start docker

# Ubuntu 22.04
sudo snap install docker