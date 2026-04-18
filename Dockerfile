# ===== Stage 1: 构建前端 =====
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY package*.json ./
RUN npm install
COPY . .
RUN npx vite build

# ===== Stage 2: 生产镜像 =====
FROM python:3.11-slim
WORKDIR /app

# 安装后端依赖
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 安装中文字体（matplotlib K线图标题需要）
RUN apt-get update && apt-get install -y --no-install-recommends fonts-noto-cjk && rm -rf /var/lib/apt/lists/*

# 复制后端代码（含 videos/ 和 public/assets/kline/）
COPY backend/ ./backend/

# 复制启动脚本
COPY startup.sh ./
RUN chmod +x startup.sh

# 复制前端构建产物到 dist
COPY --from=frontend-builder /app/frontend/dist ./dist

# 数据库文件放在持久化目录
ENV DB_PATH=/data/shipanya.db
RUN mkdir -p /data

EXPOSE 8000

CMD ["./startup.sh"]
