#!/bin/bash
set -e

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

# 创建数据目录
mkdir -p data

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
    echo "📋 查看日志: docker compose logs -f"
    echo "🛑 停止服务: docker compose down"
else
    echo "❌ 服务启动失败，请查看日志"
    docker compose logs
    exit 1
fi
