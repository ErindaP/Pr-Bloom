import sqlite3

DB_PATH = "smash_pr.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id TEXT PRIMARY KEY,
        tag TEXT NOT NULL
    );
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tournament TEXT,
        p1_id TEXT,
        p2_id TEXT,
        p1_character TEXT,
        p2_character TEXT,
        p1_win INTEGER
    );
    """)
    conn.commit()
    conn.close()
