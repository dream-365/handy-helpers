# install kubectl
PROXY="--socks5 127.0.0.1:1080"
curl $PROXY -LO https://dl.k8s.io/release/v1.30.0/bin/linux/amd64/kubectl
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl


# create an Aliyun ACR secret
kubectl create secret docker-registry aliyun \
    --docker-server=registry-vpc.cn-hangzhou.aliyuncs.com \
    --docker-username=<user-name> \
    --docker-password=<password> \
    --docker-email=<email>
