#!/bin/bash
set -e

# 初始化数据库并播种基础题目
cd /app/backend
python3 init_db.py

# 如果还没有 K 线动态题目，生成它们（使用 DB_PATH 环境变量）
export DB_PATH="/data/shipanya.db"
python3 -c "
import sqlite3, os
db = os.environ.get('DB_PATH', '/data/shipanya.db')
conn = sqlite3.connect(db)
c = conn.cursor()
c.execute(\"SELECT COUNT(*) FROM questions WHERE id LIKE 'kg_q%'\")
count = c.fetchone()[0]
conn.close()
if count == 0:
    print('No K-line questions found, generating from API...')
    exit(1)
print(f'Already have {count} K-line questions, skipping generation.')
" 2>/dev/null

if [ $? -ne 0 ]; then
    cd /app/backend
    python3 generate_kline_questions.py || echo "Warning: K-line generation failed, continuing anyway"
fi

# 启动 FastAPI 服务
exec python3 main.py
