install_docker = """
sudo dnf config-manager --add-repo=https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
sudo dnf -y install dnf-plugin-releasever-adapter --repo alinux3-plus
sudo dnf -y install docker-ce --nobest
sudo systemctl start docker
"""

_setup_image_proxy = """
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{{
  "registry-mirrors": ["{0}"]
}}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
"""

def setup_image_proxy(url):
    return _setup_image_proxy.format(url)