import json

def parse_bracket(uploaded_file):
    raw = json.load(uploaded_file)

    players = raw["players"]  # liste de dicts avec {id, tag}
    matches = []

    for match in raw["matches"]:
        matches.append({
            "p1_id": match["p1_id"],
            "p2_id": match["p2_id"],
            "p1_character": match["p1_character"],
            "p2_character": match["p2_character"],
            "p1_win": match["p1_win"]
        })

    return matches, players
