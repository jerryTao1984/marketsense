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

COPY backend/ ./backend/

# 复制视频文件
COPY backend/videos/ ./backend/videos/

# 复制 K 线图片（后端提供）
COPY public/assets/kline/ ./backend/public/assets/kline/

# 复制前端构建产物到 dist
COPY --from=frontend-builder /app/frontend/dist ./dist

# 数据库文件放在持久化目录
ENV DB_PATH=/data/shipanya.db
RUN mkdir -p /data

EXPOSE 8000

CMD ["sh", "-c", "cd /app/backend && python3 main.py"]
