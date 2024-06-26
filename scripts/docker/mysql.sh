# 初始化
docker run --rm --name int-mysql \
-e MYSQL_ROOT_PASSWORD=my-secret-pw \
-e MYSQL_USER=example-user \
-e MYSQL_PASSWORD=my_cool_secret \
-v /data/mysql:/var/lib/mysql \
registry.openanolis.cn/openanolis/mysql:8.0.30-8.6

# 运行
docker run --name prod-mysql \
-v /data/mysql:/var/lib/mysql \
-d registry.openanolis.cn/openanolis/mysql:8.0.30-8.6