#!/bin/bash
set -e

REPO="https://github.com/jerryTao1984/marketsense.git"
APP_DIR="/opt/marketsense"

echo "🦆 识盘鸭 - 一键部署"

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

if ! command -v docker compose &> /dev/null; then
    echo "❌ Docker Compose 未安装"
    exit 1
fi

# 拉取代码
if [ -d "$APP_DIR" ]; then
    echo "📂 项目已存在，更新代码..."
    cd "$APP_DIR"
    git pull origin main
else
    echo "📥 克隆代码到 $APP_DIR ..."
    git clone $REPO $APP_DIR
    cd $APP_DIR
fi

# 创建数据目录
mkdir -p data

# 配置 Docker 镜像加速（国内服务器）
if ! sudo grep -q "registry-mirrors" /etc/docker/daemon.json 2>/dev/null; then
    echo "🔧 配置 Docker 镜像加速器..."
    sudo mkdir -p /etc/docker
    sudo tee /etc/docker/daemon.json <<'DOCKER_EOF'
{
  "registry-mirrors": [
    "https://docker.1ms.run",
    "https://docker.ketches.cn"
  ]
}
DOCKER_EOF
    sudo systemctl daemon-reload
    sudo systemctl restart docker
    echo "✅ Docker 镜像加速配置完成"
fi

# 构建并启动
echo "📦 构建镜像..."
docker compose build --no-cache

echo "🚀 启动服务..."
docker compose up -d

# 等待启动
echo "⏳ 等待服务启动..."
sleep 5

# 检查健康状态
if docker compose ps | grep -q "Up"; then
    echo "✅ 部署成功！"
    echo "🌐 访问地址: http://$(hostname -I 2>/dev/null | awk '{print $1}'):5000"
    echo "📋 查看日志: cd $APP_DIR && docker compose logs -f"
    echo "🛑 停止服务: cd $APP_DIR && docker compose down"
else
    echo "❌ 服务启动失败，请查看日志"
    docker compose logs
    exit 1
fi
