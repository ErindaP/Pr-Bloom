import sqlite3

DB_PATH = "smash_pr.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_character_elo_table():
    conn = get_connection()
    c = conn.cursor()
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

def get_elos_by_player(player_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    SELECT character, elo FROM character_elos WHERE player_id = ?
    """, (player_id,))
    results = c.fetchall()
    conn.close()
    return {char: elo for char, elo in results}

def update_character_elo(player_id, character, new_elo):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    INSERT INTO character_elos (player_id, character, elo)
    VALUES (?, ?, ?)
    ON CONFLICT(player_id, character) DO UPDATE SET elo=excluded.elo
    """, (player_id, character, new_elo))
    conn.commit()
    conn.close()
