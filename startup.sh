#!/bin/bash
set -e

export DB_PATH="/data/shipanya.db"
cd /app/backend

# 1. 生成缺失的 K 线 SVG，避免 Docker 内静态资源 404
echo "=== Step 1: Generate missing K-line SVG assets ==="
python3 generate_missing_kline_svgs.py

# 2. 初始化数据库并播种基础题目
echo "=== Step 2: Initialize database ==="
python3 init_db.py

# 3. 修复已有 P1/P2/P3 题目的 broken image_url（旧记录引用了不存在的 SVG）
echo "=== Step 3: Fix broken image URLs for P1/P2/P3 ==="
python3 -c "
import sqlite3
conn = sqlite3.connect('${DB_PATH}')
c = conn.cursor()
# 清理 init_db 中指向不存在 SVG 的旧记录
c.execute(\"UPDATE questions SET image_url = NULL, type = 'text' WHERE level_id IN ('P1','P2','P3')\")
conn.commit()
print(f'Fixed {c.rowcount} P1/P2/P3 questions')
conn.close()
"

# 4. 生成 K 线图片（PNG）
echo "=== Step 4: Generate K-line images ==="
python3 generate_kline_images.py || echo "Warning: K-line image generation failed, continuing anyway"

# 5. 生成动态 K 线题目（含 image_url 指向生成的 PNG）
echo "=== Step 5: Generate K-line questions from API ==="
python3 generate_kline_questions.py || echo "Warning: K-line question generation failed, continuing anyway"

# 6. 启动 FastAPI 服务
echo "=== Step 6: Starting server ==="
exec python3 main.py
