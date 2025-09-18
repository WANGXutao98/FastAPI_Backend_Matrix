set -x
name=fastapi_framework_8889
image_name=fastapi_framework_dev

cd ..
container_id=$(docker container ls -a -f "name=${name}" -q)
image_id=$(docker images -q ${image_name})

if [ -z "${image_id}" ]; then
    # 构建 Docker 镜像，指定 Dockerfile
    docker build -t ${image_name} -f ./docker/Dockerfile.dev .
fi

if [ -z "${container_id}" ]; then
    # 运行 Docker 容器
    docker run -itd \
    -p 8889:8888\
    --privileged \
    --name "${name}" \
    --cap-add=SYS_PTRACE \
    --mount type=bind,source=$(pwd),target=/data/app \
    ${image_name} /bin/bash

    sleep 3
    docker exec -it "${name}" /bin/bash
else
    docker exec -it "${name}" /bin/bash
fi