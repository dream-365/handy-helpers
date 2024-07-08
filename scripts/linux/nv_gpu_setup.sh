# Step 1: Install NVIDIA GPU Driver
wget https://us.download.nvidia.cn/tesla/550.54.15/NVIDIA-Linux-x86_64-550.54.15.run
chmod +x NVIDIA-Linux-x86_64-550.54.15.run
sh NVIDIA-Linux-x86_64-550.54.15.run --silent

# Step 2: Install Docker
sudo dnf config-manager --add-repo=https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
sudo dnf -y install dnf-plugin-releasever-adapter --repo alinux3-plus
sudo dnf -y install docker-ce --nobest
sudo systemctl start docker

# Step 3: Install NVIDIA container toolkit
curl -s -L https://nvidia.github.io/libnvidia-container/stable/rpm/nvidia-container-toolkit.repo | \
  sudo tee /etc/yum.repos.d/nvidia-container-toolkit.repo
sudo yum install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker