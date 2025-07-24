from utils.startgg_api import fetch_tournament_sets, transform_to_local_format
from db.database import get_connection
from db.character_elos import update_character_elo
from logic.elo import update_elo
from utils.character_mapping import get_character_name

INITIAL_ELO = 1500

# dictionnaire temporaire pour les elos avant insertion
elos = {}

def insert_players_into_db(players):
    conn = get_connection()
    c = conn.cursor()
    for p in players:
        c.execute("""
        INSERT OR IGNORE INTO players (id, tag) VALUES (?, ?)
        """, (p['id'], p['tag']))
    conn.commit()
    conn.close()

def insert_match_into_db(tournament_name, match):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    INSERT INTO matches (tournament, p1_id, p2_id, p1_character, p2_character, p1_win)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        tournament_name,
        match['p1_id'],
        match['p2_id'],
        match['p1_character'],
        match['p2_character'],
        int(match['p1_win'])
    ))
    conn.commit()
    conn.close()

def process_and_store_elo(match):
    p1_id, p2_id = match['p1_id'], match['p2_id']
    char1 = get_character_name(match['p1_character'])
    char2 = get_character_name(match['p2_character'])
    
    key1 = (p1_id, char1)
    key2 = (p2_id, char2)

    if key1 not in elos:
        elos[key1] = INITIAL_ELO
    if key2 not in elos:
        elos[key2] = INITIAL_ELO

    result = 1 if match['p1_win'] else 0
    new_elo1, new_elo2 = update_elo(elos[key1], elos[key2], result)
    elos[key1] = new_elo1
    elos[key2] = new_elo2


def import_tournament(slug):
    tournament_name, raw_sets = fetch_tournament_sets(slug)
    players, matches = transform_to_local_format(raw_sets)

    insert_players_into_db(players)

    for match in matches:
        insert_match_into_db(tournament_name, match)
        process_and_store_elo(match)

    for (player_id, character), elo in elos.items():
        update_character_elo(player_id, character, elo)

    return tournament_name, len(matches), len(players)
