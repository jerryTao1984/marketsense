#!/bin/bash
set -e

echo "🦆 识盘鸭 - 更新服务"

# 拉取最新代码
echo "📥 拉取最新代码..."
git pull origin main

# 重新构建并启动
echo "📦 重新构建镜像..."
docker compose build --no-cache

echo "🔄 重启服务..."
docker compose up -d

# 等待启动
echo "⏳ 等待服务启动..."
sleep 5

# 检查健康状态
if docker compose ps | grep -q "Up"; then
    echo "✅ 更新成功！"
    echo "🌐 访问地址: http://$(hostname -I 2>/dev/null | awk '{print $1}'):5000"
    echo "📋 查看日志: docker compose logs -f"
else
    echo "❌ 服务启动失败，请查看日志"
    docker compose logs
    exit 1
fi
