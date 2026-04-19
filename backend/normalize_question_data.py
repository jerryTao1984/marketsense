"""
Normalize generated question data so startup is deterministic even with an old DB volume.
"""
from __future__ import annotations

import os
import sqlite3


DB_PATH = os.environ.get("DB_PATH", "shipanya.db")


def main() -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Historical bug: generated trend questions used a non-existent level_id "predict".
    cursor.execute("UPDATE questions SET level_id = 'P1' WHERE level_id = 'predict'")
    remapped_predict = cursor.rowcount

    # Seeded P1/P2/P3 questions are text-only templates. If an old DB volume still has stale
    # image_url values on these rows, clear them to avoid arbitrary/wrong image reuse.
    cursor.execute("""
        UPDATE questions
        SET image_url = NULL, type = 'text'
        WHERE id GLOB 'p[123]_q*'
    """)
    cleared_seed_predict = cursor.rowcount

    # Generated questions with a real image path should use type=image. If image_url is empty,
    # keep them as text so the frontend won't expect a chart.
    cursor.execute("""
        UPDATE questions
        SET type = CASE
            WHEN image_url LIKE '/assets/kline/%' THEN 'image'
            ELSE 'text'
        END
        WHERE id LIKE 'kg_q%' OR id LIKE 'enh_%'
    """)
    normalized_generated = cursor.rowcount

    # Remove rows that still point to non-existent levels.
    cursor.execute("""
        DELETE FROM questions
        WHERE level_id NOT IN (SELECT id FROM levels)
    """)
    deleted_orphans = cursor.rowcount

    conn.commit()
    conn.close()

    print(
        "Question normalization summary: "
        f"remapped_predict={remapped_predict}, "
        f"cleared_seed_predict={cleared_seed_predict}, "
        f"normalized_generated={normalized_generated}, "
        f"deleted_orphans={deleted_orphans}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
