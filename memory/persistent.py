import sqlite3
from pathlib import Path


DB_PATH = Path("memory.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS memory (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)

    conn.commit()
    conn.close()


def set_memory(key: str, value: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO memory (key, value)
    VALUES (?, ?)
    ON CONFLICT(key)
    DO UPDATE SET value = excluded.value
    """, (key, value))

    conn.commit()
    conn.close()


def get_memory(key: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT value FROM memory WHERE key = ?", (key,))
    row = cur.fetchone()

    conn.close()

    if row:
        return row[0]

    return None