import sqlite3

DB_PATH = "smash_pr.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Table joueurs
    c.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id TEXT PRIMARY KEY,
        tag TEXT NOT NULL
    );
    """)

    # Table matches
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

    # Table Elos par personnage
    c.execute("""
    CREATE TABLE IF NOT EXISTS character_elos (
        player_id TEXT NOT NULL,
        character TEXT NOT NULL,
        elo INTEGER NOT NULL,
        PRIMARY KEY (player_id, character)
    );
    """)

    conn.commit()
    conn.close()
