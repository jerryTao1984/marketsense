#!/bin/bash
set -e

export DB_PATH="/data/shipanya.db"
cd /app/backend

run_optional_step() {
  local label="$1"
  shift
  echo "=== ${label} ==="
  if "$@"; then
    echo "✓ ${label} succeeded"
    return 0
  fi
  local code=$?
  echo "⚠ ${label} failed with exit code ${code}"
  return ${code}
}

# 1. 生成缺失的 K 线 SVG，避免 Docker 内静态资源 404
echo "=== Step 1: Generate missing K-line SVG assets ==="
python3 generate_missing_kline_svgs.py

# 2. 初始化数据库并播种基础题目
echo "=== Step 2: Initialize database ==="
python3 init_db.py

echo "=== Step 2.5: Expand questions ==="
run_optional_step "Expand questions 1" python3 expand_questions.py || true
run_optional_step "Expand questions 2" python3 expand_questions_v2.py || true
run_optional_step "Expand enhanced K-line questions" python3 expand_enhanced_kline.py || true
run_optional_step "Expand money flow questions" python3 expand_moneyflow.py || true

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
run_optional_step "Step 4: Generate K-line images" python3 generate_kline_images.py || true

# 5. 生成动态 K 线题目（含 image_url 指向生成的 PNG）
run_optional_step "Step 5: Generate K-line questions from API" python3 generate_kline_questions.py || true

# 6. 归一化旧库里的脏数据，避免错误 level_id / 错误图片残留
echo "=== Step 6: Normalize question data ==="
python3 normalize_question_data.py

# 7. 清理失效 image_url，避免前端渲染坏图
echo "=== Step 7: Verify K-line assets and clear broken references ==="
python3 verify_kline_assets.py --fix-db

# 8. 打印题库摘要，方便从 docker logs 直接排查
echo "=== Step 8: Report question summary ==="
python3 report_question_summary.py

# 9. 启动 FastAPI 服务
echo "=== Step 9: Starting server ==="
exec python3 main.py
