#!/bin/bash
set -e

export DB_PATH="/data/shipanya.db"
cd /app/backend

# 初始化数据库并播种基础题目
python3 init_db.py

# 检查是否已有 K 线动态题目
COUNT=$(python3 -c "
import sqlite3
conn = sqlite3.connect('${DB_PATH}')
c = conn.cursor()
c.execute(\"SELECT COUNT(*) FROM questions WHERE id LIKE 'kg_q%'\")
print(c.fetchone()[0])
conn.close()
")

if [ "$COUNT" -eq 0 ]; then
    echo "No K-line questions found, generating from API..."
    python3 generate_kline_questions.py || echo "Warning: K-line generation failed, continuing anyway"
else
    echo "Already have $COUNT K-line questions, skipping generation."
fi

# 启动 FastAPI 服务
exec python3 main.py
