"""
识盘鸭 V1.0 FastAPI 后端
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sqlite3
import json
import os
import random

app = FastAPI(title="识盘鸭 MVP API")

# CORS - 允许前端跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.environ.get('DB_PATH', os.path.join(os.path.dirname(__file__), 'shipanya.db'))


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def migrate_db():
    """数据库迁移：添加手机号、昵称、答题记录等字段"""
    conn = get_db()
    cursor = conn.cursor()
    # 添加 phone 和 nickname 列
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN phone TEXT DEFAULT NULL")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN nickname TEXT DEFAULT NULL")
    except Exception:
        pass
    # 添加 completed_at 列
    try:
        cursor.execute("ALTER TABLE user_progress ADD COLUMN completed_at TIMESTAMP DEFAULT NULL")
    except Exception:
        pass
    # 创建唯一索引
    cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_user_progress_user_level ON user_progress(user_id, level_id)")
    # 创建 answer_history 表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS answer_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            question_id TEXT NOT NULL,
            level_id TEXT NOT NULL,
            category_id TEXT NOT NULL,
            user_answer TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            is_correct INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    # 创建 quiz_session 表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_session (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            level_id TEXT NOT NULL,
            correct_count INTEGER DEFAULT 0,
            total_count INTEGER DEFAULT 0,
            passed INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()
    print("Database migration completed.")


# ===== 请求模型 =====
class AuthSync(BaseModel):
    device_id: str


class PhoneLogin(BaseModel):
    phone: str


class AnswerSubmit(BaseModel):
    question_id: str
    user_answer: str
    user_id: int = 0


class LevelComplete(BaseModel):
    user_id: int
    level_id: str
    correct_count: int
    total_count: int


def get_unlocked_levels(cursor, user_id, completed):
    """获取已解锁的关卡"""
    unlocked = {}
    for cat in ['basics', 'trading', 'kline', 'predict']:
        cursor.execute("""
            SELECT id, sort_order FROM levels WHERE category_id = ? ORDER BY sort_order
        """, (cat,))
        levels = cursor.fetchall()
        unlocked_levels = []
        for i, level in enumerate(levels):
            if i == 0 or level["id"] in completed:
                unlocked_levels.append(level["id"])
        unlocked[cat] = unlocked_levels
    return unlocked


# ===== 1. 静默登录与状态同步 =====
@app.post("/api/v1/auth/sync")
async def auth_sync(data: AuthSync):
    """静默登录：根据 device_id 返回用户状态"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE device_id = ?", (data.device_id,))
    user = cursor.fetchone()

    if not user:
        cursor.execute(
            "INSERT INTO users (device_id) VALUES (?)",
            (data.device_id,)
        )
        conn.commit()
        user_id = cursor.lastrowid
    else:
        user_id = user["id"]

    cursor.execute("SELECT hearts, streak_days FROM users WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()

    cursor.execute("""
        SELECT level_id FROM user_progress WHERE user_id = ? AND is_completed = 1
    """, (user_id,))
    completed = [row["level_id"] for row in cursor.fetchall()]

    unlocked = get_unlocked_levels(cursor, user_id, completed)
    conn.close()

    return {
        "user_id": user_id,
        "hearts": user_data["hearts"],
        "streak_days": user_data["streak_days"],
        "unlocked_levels": unlocked,
    }


# ===== 1b. 手机号登录 =====
@app.post("/api/v1/auth/phone-login")
async def phone_login(data: PhoneLogin):
    """手机号登录：自动创建或登录"""
    if not data.phone or len(data.phone) != 11 or not data.phone.isdigit():
        raise HTTPException(status_code=400, detail="请输入正确的11位手机号")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE phone = ?", (data.phone,))
    user = cursor.fetchone()

    if not user:
        nickname = f"用户{data.phone[-4:]}"
        cursor.execute(
            "INSERT INTO users (phone, nickname) VALUES (?, ?)",
            (data.phone, nickname)
        )
        conn.commit()
        user_id = cursor.lastrowid
    else:
        user_id = user["id"]

    cursor.execute("SELECT hearts, streak_days, nickname FROM users WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()

    cursor.execute("""
        SELECT level_id FROM user_progress WHERE user_id = ? AND is_completed = 1
    """, (user_id,))
    completed = [row["level_id"] for row in cursor.fetchall()]

    unlocked = get_unlocked_levels(cursor, user_id, completed)
    conn.close()

    return {
        "user_id": user_id,
        "hearts": user_data["hearts"],
        "streak_days": user_data["streak_days"],
        "nickname": user_data["nickname"],
        "unlocked_levels": unlocked,
    }


# ===== 2. 获取分区信息 =====
@app.get("/api/v1/categories")
async def get_categories():
    """获取所有分区和关卡列表"""
    conn = get_db()
    cursor = conn.cursor()

    categories = {}
    cursor.execute("SELECT id, category_id, name, description, sort_order FROM levels ORDER BY category_id, sort_order")
    for row in cursor.fetchall():
        cat = row["category_id"]
        if cat not in categories:
            category_info = {
                'basics': {'id': 'basics', 'name': '基础概念', 'icon': '📖'},
                'trading': {'id': 'trading', 'name': '交易法则', 'icon': '🐢'},
                'kline': {'id': 'kline', 'name': 'K线实盘', 'icon': '📊'},
                'predict': {'id': 'predict', 'name': 'K线预测', 'icon': '🔮'},
            }[cat]
            categories[cat] = {**category_info, 'levels': []}

        level_data = {
            'id': row["id"],
            'name': row["name"],
            'description': row["description"],
            'sort_order': row["sort_order"],
        }
        if cat == 'trading':
            video_url = TRADING_VIDEOS.get(row["id"])
            if video_url:
                level_data['video_url'] = video_url
        categories[cat]['levels'].append(level_data)

    conn.close()
    return list(categories.values())


# ===== 3. 获取关卡题目 =====
@app.get("/api/v1/questions/{level_id}")
async def get_questions(level_id: str):
    """获取指定关卡的题目列表（不包含正确答案）"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, type, title, image_url, options_json, sort_order
        FROM questions WHERE level_id = ? ORDER BY sort_order
    """, (level_id,))
    rows = cursor.fetchall()

    if not rows:
        conn.close()
        raise HTTPException(status_code=404, detail="关卡不存在或没有题目")

    # 打乱题目顺序
    rows = list(rows)
    random.shuffle(rows)

    questions = []
    for row in rows:
        options = json.loads(row["options_json"])
        # 打乱选项顺序
        random.shuffle(options)
        # 不返回正确答案，防止前端被抓包作弊
        questions.append({
            "id": row["id"],
            "type": row["type"],
            "title": row["title"],
            "image_url": row["image_url"],
            "options": options,
        })

    conn.close()
    return {
        "level_id": level_id,
        "questions": questions,
        "total": len(questions),
    }


# ===== 4. 提交答案判定 =====
@app.post("/api/v1/questions/check")
async def check_answer(submit: AnswerSubmit):
    """判定答案并返回解析"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT q.answer, q.explanation, q.level_id, l.category_id
        FROM questions q JOIN levels l ON q.level_id = l.id
        WHERE q.id = ?
    """, (submit.question_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="题目不存在")

    is_correct = submit.user_answer == row["answer"]

    # 记录答题历史
    if submit.user_id > 0:
        cursor.execute("""
            INSERT INTO answer_history (user_id, question_id, level_id, category_id,
                                         user_answer, correct_answer, is_correct)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (submit.user_id, submit.question_id, row["level_id"], row["category_id"],
              submit.user_answer, row["answer"], is_correct))
        conn.commit()

    conn.close()
    return {
        "is_correct": is_correct,
        "correct_answer": row["answer"],
        "explanation": row["explanation"],
        "level_id": row["level_id"],
        "category_id": row["category_id"],
    }


# ===== 5. 关卡结算 =====
@app.post("/api/v1/progress/complete")
async def complete_level(data: LevelComplete):
    """结算关卡，更新进度和解锁下一关"""
    conn = get_db()
    cursor = conn.cursor()

    # 检查用户是否存在
    cursor.execute("SELECT id FROM users WHERE id = ?", (data.user_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="用户不存在")

    # 判断是否通过（>=60% 正确率）
    passed = data.correct_count >= int(data.total_count * 0.6)

    # 记录答题会话
    cursor.execute("""
        INSERT INTO quiz_session (user_id, level_id, correct_count, total_count, passed)
        VALUES (?, ?, ?, ?, ?)
    """, (data.user_id, data.level_id, data.correct_count, data.total_count, passed))

    if passed:
        # 更新或插入进度
        cursor.execute("""
            INSERT INTO user_progress (user_id, level_id, is_completed, best_score, completed_at)
            VALUES (?, ?, 1, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id, level_id) DO UPDATE SET is_completed=1, best_score=max(excluded.best_score, user_progress.best_score), completed_at=CURRENT_TIMESTAMP
        """, (data.user_id, data.level_id, data.correct_count))

        # 更新 streak（同一天只 +1）
        cursor.execute("""
            SELECT COUNT(*) as cnt FROM user_progress
            WHERE user_id = ? AND DATE(completed_at) = DATE('now')
        """, (data.user_id,))
        today_completions = cursor.fetchone()["cnt"]
        if today_completions == 0:
            cursor.execute("""
                UPDATE users SET streak_days = streak_days + 1 WHERE id = ?
            """, (data.user_id,))

        # 查找下一关
        cursor.execute("""
            SELECT id FROM levels
            WHERE category_id = (SELECT category_id FROM levels WHERE id = ?)
              AND sort_order > (SELECT sort_order FROM levels WHERE id = ?)
            ORDER BY sort_order LIMIT 1
        """, (data.level_id, data.level_id))
        next_level = cursor.fetchone()

        next_unlocked = next_level["id"] if next_level else None

    else:
        # 未通过也记录进度（取最高分）
        cursor.execute("""
            INSERT INTO user_progress (user_id, level_id, is_completed, best_score, completed_at)
            VALUES (?, ?, 0, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id, level_id) DO UPDATE SET best_score=max(excluded.best_score, user_progress.best_score)
        """, (data.user_id, data.level_id, data.correct_count))

        next_unlocked = None

    # 恢复体力（通关恢复1颗心）
    if passed:
        cursor.execute("""
            UPDATE users SET hearts = MIN(5, hearts + 1) WHERE id = ?
        """, (data.user_id,))

    conn.commit()

    # 获取最新体力
    cursor.execute("SELECT hearts, streak_days FROM users WHERE id = ?", (data.user_id,))
    user_data = cursor.fetchone()
    conn.close()

    return {
        "passed": passed,
        "correct_count": data.correct_count,
        "total_count": data.total_count,
        "next_unlocked": next_unlocked,
        "hearts": user_data["hearts"],
        "streak_days": user_data["streak_days"],
    }


# ===== 6. 扣除体力 =====
@app.post("/api/v1/user/deduct-heart")
async def deduct_heart(user_id: int):
    """答错时扣除1颗心"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT hearts FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="用户不存在")

    if user["hearts"] > 0:
        cursor.execute("UPDATE users SET hearts = hearts - 1 WHERE id = ?", (user_id,))
        conn.commit()

    cursor.execute("SELECT hearts FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()

    return {"hearts": result["hearts"]}


# ===== 7. 恢复体力 =====
@app.post("/api/v1/user/refill-hearts")
async def refill_hearts(user_id: int):
    """恢复满体力"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET hearts = 5 WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

    return {"hearts": 5}


# ===== 8. 用户资料与统计 =====
@app.get("/api/v1/user/profile")
async def get_user_profile(user_id: int):
    """获取用户信息 + 总体正确率 + 每关卡正确率"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, phone, nickname, hearts, streak_days, created_at FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="用户不存在")

    # 总体正确率
    cursor.execute("""
        SELECT COUNT(*) as total_attempts, SUM(is_correct) as correct_count
        FROM answer_history WHERE user_id = ?
    """, (user_id,))
    stats = cursor.fetchone()
    total_attempts = stats["total_attempts"] or 0
    total_correct = stats["correct_count"] or 0
    accuracy = round(100.0 * total_correct / max(total_attempts, 1), 1)

    # 每关卡正确率
    cursor.execute("""
        SELECT level_id,
               COUNT(*) as total,
               SUM(is_correct) as correct,
               ROUND(100.0 * SUM(is_correct) / COUNT(*), 1) as accuracy
        FROM answer_history
        WHERE user_id = ?
        GROUP BY level_id
    """, (user_id,))
    level_stats = [dict(row) for row in cursor.fetchall()]

    # 历史答题会话
    cursor.execute("""
        SELECT level_id, correct_count, total_count, passed, created_at
        FROM quiz_session
        WHERE user_id = ?
        ORDER BY created_at DESC LIMIT 20
    """, (user_id,))
    sessions = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return {
        "id": user["id"],
        "phone": user["phone"],
        "nickname": user["nickname"],
        "hearts": user["hearts"],
        "streak_days": user["streak_days"],
        "created_at": user["created_at"],
        "total_attempts": total_attempts,
        "total_correct": total_correct,
        "overall_accuracy": accuracy,
        "level_stats": level_stats,
        "sessions": sessions,
    }


# ===== 9. 错题本 =====
@app.get("/api/v1/user/wrong-answers")
async def get_wrong_answers(user_id: int, level_id: str = None):
    """获取所有错题（含题目详情），支持按 level_id 过滤"""
    conn = get_db()
    cursor = conn.cursor()

    query = """
        SELECT ah.id as record_id, ah.question_id, ah.level_id, ah.category_id,
               ah.user_answer, ah.correct_answer, ah.created_at,
               q.title, q.explanation, q.options_json
        FROM answer_history ah
        JOIN questions q ON ah.question_id = q.id
        WHERE ah.user_id = ? AND ah.is_correct = 0
    """
    params = [user_id]
    if level_id:
        query += " AND ah.level_id = ?"
        params.append(level_id)

    query += " ORDER BY ah.created_at DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()

    results = []
    for row in rows:
        results.append({
            "record_id": row["record_id"],
            "question_id": row["question_id"],
            "level_id": row["level_id"],
            "category_id": row["category_id"],
            "user_answer": row["user_answer"],
            "correct_answer": row["correct_answer"],
            "created_at": row["created_at"],
            "title": row["title"],
            "explanation": row["explanation"],
            "options": json.loads(row["options_json"]),
        })

    conn.close()
    return results


# ===== 10. 已答对的题目 =====
@app.get("/api/v1/user/done-questions")
async def get_done_questions(user_id: int, level_id: str = None):
    """获取用户已答对的题目ID列表（这些题不再出现）"""
    conn = get_db()
    cursor = conn.cursor()

    query = """
        SELECT DISTINCT question_id FROM answer_history
        WHERE user_id = ? AND is_correct = 1
    """
    params = [user_id]
    if level_id:
        query += " AND level_id = ?"
        params.append(level_id)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [row["question_id"] for row in rows]


@app.get("/api/v1/user/attempted-questions")
async def get_attempted_questions(user_id: int, level_id: str = None):
    """获取用户所有答过的题目ID列表（无论对错，用于复习模式）"""
    conn = get_db()
    cursor = conn.cursor()

    query = """
        SELECT DISTINCT question_id FROM answer_history
        WHERE user_id = ?
    """
    params = [user_id]
    if level_id:
        query += " AND level_id = ?"
        params.append(level_id)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [row["question_id"] for row in rows]


@app.get("/api/v1/user/review-questions")
async def get_review_questions(user_id: int, level_id: str = None):
    """获取用户所有做过的题目详情（无论对错，用于复习模式）"""
    conn = get_db()
    cursor = conn.cursor()

    query = """
        SELECT DISTINCT q.id, q.title, q.options_json, q.answer, q.explanation,
               q.level_id, q.category_id, q.type, q.image_url
        FROM answer_history ah
        JOIN questions q ON ah.question_id = q.id
        WHERE ah.user_id = ?
    """
    params = [user_id]
    if level_id:
        query += " AND ah.level_id = ?"
        params.append(level_id)

    query += " ORDER BY q.id"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        results.append({
            "id": row["id"],
            "type": row["type"],
            "title": row["title"],
            "image_url": row["image_url"],
            "options": json.loads(row["options_json"]),
            "answer": row["answer"],
            "explanation": row["explanation"],
            "level_id": row["level_id"],
            "category_id": row["category_id"],
        })
    return results


# ===== 11. 做题记录 =====
@app.get("/api/v1/user/history")
async def get_history(user_id: int, level_id: str = None):
    """获取用户所有做题记录，按关卡分组"""
    conn = get_db()
    cursor = conn.cursor()

    query = """
        SELECT ah.id as record_id, ah.question_id, ah.level_id, ah.category_id,
               ah.user_answer, ah.correct_answer, ah.is_correct, ah.created_at,
               q.title
        FROM answer_history ah
        JOIN questions q ON ah.question_id = q.id
        WHERE ah.user_id = ?
    """
    params = [user_id]
    if level_id:
        query += " AND ah.level_id = ?"
        params.append(level_id)

    query += " ORDER BY ah.created_at DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()

    results = []
    for row in rows:
        results.append({
            "record_id": row["record_id"],
            "question_id": row["question_id"],
            "level_id": row["level_id"],
            "category_id": row["category_id"],
            "user_answer": row["user_answer"],
            "correct_answer": row["correct_answer"],
            "is_correct": row["is_correct"],
            "created_at": row["created_at"],
            "title": row["title"],
        })

    conn.close()
    return results


# ===== 生产模式：FastAPI 直接 serve 前端静态文件 =====
# Docker 部署时只需一个端口 8000

# 交易法则关卡视频
TRADING_VIDEOS = {
    'T1': '/videos/dolphin_trading.mp4',
    'T2': '/videos/turtle_trading.mp4',
}

try:
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import FileResponse

    # 挂载视频目录
    _videos_dir = os.path.join(os.path.dirname(__file__), 'videos')
    if os.path.isdir(_videos_dir):
        app.mount("/videos", StaticFiles(directory=_videos_dir), name="videos")
        print(f"✅ Serving videos from: {_videos_dir}")

    # 挂载 K 线图片（本地开发用 ../public/assets/kline，Docker 用 backend 内相对路径）
    _kline_candidates = [
        os.path.join(os.path.dirname(__file__), 'public', 'assets', 'kline'),  # Docker
        os.path.join(os.path.dirname(__file__), '..', 'public', 'assets', 'kline'),  # 本地开发
    ]
    _kline_dir = None
    for p in _kline_candidates:
        if os.path.isdir(p):
            _kline_dir = p
            break
    if _kline_dir:
        app.mount("/assets/kline", StaticFiles(directory=_kline_dir), name="kline")
        print(f"✅ Serving kline images from: {_kline_dir}")

    # 支持多种路径：Docker 容器 /app/dist 或 本地开发 ../dist
    _dist_candidates = [
        os.path.join(os.path.dirname(__file__), '..', 'dist'),  # 本地开发
        '/app/dist',                                              # Docker 容器
    ]
    FRONTEND_DIST = None
    for p in _dist_candidates:
        if os.path.isdir(os.path.join(p, 'assets')) or os.path.isfile(os.path.join(p, 'index.html')):
            FRONTEND_DIST = os.path.abspath(p)
            break

    if FRONTEND_DIST:
        print(f"✅ Serving frontend from: {FRONTEND_DIST}")
        app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")), name="assets")

        @app.get("/{full_path:path}")
        async def serve_spa(full_path: str):
            """SPA 路由回退到 index.html"""
            if full_path.startswith('api/'):
                raise HTTPException(status_code=404)
            file_path = os.path.join(FRONTEND_DIST, full_path)
            if os.path.isfile(file_path):
                return FileResponse(file_path)
            return FileResponse(os.path.join(FRONTEND_DIST, 'index.html'))
    else:
        print("⚠️  Frontend dist not found, running in API-only mode")
except Exception as e:
    print(f"⚠️  Failed to mount frontend: {e}")


# ===== 数据库初始化 + 迁移（模块加载时执行） =====
from init_db import init_db, seed_levels_and_questions

init_db()

# 数据为空时自动塞入题目
try:
    _conn = get_db()
    _cnt = _conn.execute("SELECT COUNT(*) FROM levels").fetchone()[0]
    _conn.close()
    if _cnt == 0:
        print("No levels found, seeding...")
        seed_levels_and_questions()
except Exception as e:
    print(f"Seed check skipped: {e}")

migrate_db()


# ===== 本地开发 =====
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
