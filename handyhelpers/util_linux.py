import os

class CommandGenerator:
    def __init__(self):
      pass

    def generate_install_docker_command(self):
        return """
yum install epel-release -y
yum install docker -y
systemctl start docker
"""

    def generate_config_github(self):
        return """
git config --global user.name notebook
git config --global user.email notebook@email.com

cat > ~/.ssh/id_ed25519 << EOF
{ssh_private_key}
EOF

cat > ~/.ssh/config << EOF
Host *
    StrictHostKeyChecking no
EOF

chmod 400 ~/.ssh/id_ed25519
chmod 400 ~/.ssh/config
        """.format(ssh_private_key=os.environ.get("SSH_PRIVATE_KEY"))

    def generate_install_proxy_command(self):
        return """
sudo docker run -e PASSWORD="passIt2020" \
-e METHOD="aes-256-cfb" \
-p8000:8388 -p8000:8388/udp \
-d shadowsocks/shadowsocks-libev
        """

    def generate_install_git_command(self):
        return "yum install git -y"

    def generate_start_jupyter_command(self, name="base-notebook"):
        return """
mkdir -p /root/work
cd /root/work

docker run -itd --rm -p 10000:8888 \
    --name notebook \
    -v "${{PWD}}":/home/jovyan/work \
    --user root \
    -e CHOWN_EXTRA="/home/jovyan/work" \
    -e CHOWN_EXTRA_OPTS="-R" \
    quay.io/jupyter/{name} \
    start-notebook.py --ServerApp.token=abcd

docker exec -u jovyan notebook bash -c "mkdir ~/.ssh
{config_github_cmd}"
""".format(name=name, config_github_cmd=self.generate_config_github())