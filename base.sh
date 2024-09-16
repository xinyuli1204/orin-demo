#!/bin/bash

# SSH 连接到服务器
# 替换 USERNAME、HOST 和 PORT 为你的 SSH 服务器的实际用户名、主机名和端口号
# 使用正确的密钥文件路径替换 YOUR_SSH_KEY.pem
ssh xinyu@192.168.61.44

# 你可以在这里执行服务器上需要运行的任何命令
# 例如，启动一个 Docker 容器

# 检查 Docker 是否运行

# 运行 Docker 容器
# 替换 CONTAINER_NAME 和 IMAGE_NAME 为你的容器名和镜像名
docker start ros-dev-macos
docker exec -it ros-dev-macos bash -c 'echo hello'

# 断开 SSH 连接
exit
EOF

echo "Docker container started remotely."