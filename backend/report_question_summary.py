"""
Print a compact startup summary for question counts and K-line image coverage.
"""
from __future__ import annotations

import os
import sqlite3


DB_PATH = os.environ.get("DB_PATH", "shipanya.db")


def main() -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Question summary by level:")
    cursor.execute("""
        SELECT level_id, COUNT(*) AS total,
               SUM(CASE WHEN image_url LIKE '/assets/kline/%' THEN 1 ELSE 0 END) AS with_kline_image
        FROM questions
        GROUP BY level_id
        ORDER BY level_id
    """)
    for level_id, total, with_kline_image in cursor.fetchall():
        print(f"  {level_id}: total={total}, with_kline_image={with_kline_image or 0}")

    cursor.execute("""
        SELECT COUNT(*)
        FROM questions
        WHERE image_url LIKE '/assets/kline/%'
    """)
    total_kline_refs = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM questions
        WHERE id GLOB 'p[123]_q*' AND image_url IS NOT NULL
    """)
    stale_seed_predict_images = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM questions
        WHERE level_id = 'predict'
    """)
    invalid_predict_level = cursor.fetchone()[0]

    print(
        "Question integrity summary: "
        f"total_kline_refs={total_kline_refs}, "
        f"stale_seed_predict_images={stale_seed_predict_images}, "
        f"invalid_predict_level={invalid_predict_level}"
    )

    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
