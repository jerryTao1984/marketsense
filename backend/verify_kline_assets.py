"""
Verify that every question.image_url under /assets/kline points to a real static file.
Optionally clear broken references so the frontend won't render missing images.
"""
from __future__ import annotations

import argparse
import os
import sqlite3
from collections import Counter


DB_PATH = os.environ.get("DB_PATH", "shipanya.db")


def find_assets_dir() -> str:
    candidates = [
        os.path.join(os.path.dirname(__file__), "public", "assets", "kline"),
        os.path.join(os.path.dirname(__file__), "..", "public", "assets", "kline"),
    ]
    for path in candidates:
        if os.path.isdir(path):
            return os.path.abspath(path)
    return os.path.abspath(candidates[0])


def verify(fix_db: bool = False) -> tuple[int, int]:
    assets_dir = find_assets_dir()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, level_id, image_url
        FROM questions
        WHERE image_url LIKE '/assets/kline/%'
    """)
    rows = cursor.fetchall()

    missing_rows = []
    by_level = Counter()
    for q_id, level_id, image_url in rows:
        filename = image_url.rsplit("/", 1)[-1]
        file_path = os.path.join(assets_dir, filename)
        if not os.path.isfile(file_path):
            missing_rows.append((q_id, image_url))
            by_level[level_id] += 1

    total = len(rows)
    missing = len(missing_rows)
    print(f"K-line asset verification: total_refs={total}, missing_refs={missing}, assets_dir={assets_dir}")
    if missing:
        for level_id, count in sorted(by_level.items()):
            print(f"  missing in {level_id}: {count}")
        for q_id, image_url in missing_rows[:20]:
            print(f"  broken: {q_id} -> {image_url}")

    if fix_db and missing_rows:
        cursor.executemany("UPDATE questions SET image_url = NULL WHERE id = ?", [(q_id,) for q_id, _ in missing_rows])
        conn.commit()
        print(f"Cleared broken image_url for {missing} questions")

    conn.close()
    return total, missing


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fix-db", action="store_true", help="Clear broken question.image_url values")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when broken references exist")
    args = parser.parse_args()

    _, missing = verify(fix_db=args.fix_db)
    if args.strict and missing:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
