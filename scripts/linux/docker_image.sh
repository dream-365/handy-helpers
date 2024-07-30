# 登录阿里云Docker Registry
USER_NAME=[user-name]
IMAGE_ID=[image-id]
IMAGE_NAME=[image-name]
IAMGE_VER=[image-version]
REGION_ID=cn-hangzhou
NAME_SPACE=[namespace]

docker login --username=$USER_NAME registry.$REGION_ID.aliyuncs.com
docker tag $IMAGE_ID registry.$REGION_ID.aliyuncs.com/$NAME_SPACE/$IMAGE_NAME:$IAMGE_VER
docker push registry.$REGION_ID.aliyuncs.com/$NAME_SPACE/$IMAGE_NAME:$IAMGE_VER