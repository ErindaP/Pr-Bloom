import pandas as pd
from logic.elo import update_elo

def compute_power_ranking(matches, players):
    # Exemple simplifié : Elo initial 1500
    elos = {}
    pr_points = {p['id']: 0 for p in players}

    for match in matches:
        p1, p2 = match['p1_id'], match['p2_id']
        c1, c2 = match['p1_character'], match['p2_character']
        key1 = (p1, c1)
        key2 = (p2, c2)

        elos.setdefault(key1, 1500)
        elos.setdefault(key2, 1500)

        r1 = 1 if match['p1_win'] else 0
        elos[key1], elos[key2] = update_elo(elos[key1], elos[key2], r1)

        # Bonus Upset simplifié
        diff = abs(elos[key1] - elos[key2])
        upset_bonus = max(0, diff // 25)
        winner = p1 if match['p1_win'] else p2
        pr_points[winner] += 10 + upset_bonus

    data = [{
        "Tag": next(p['tag'] for p in players if p['id'] == pid),
        "PR Points": pts
    } for pid, pts in pr_points.items()]
    
    return pd.DataFrame(data).sort_values(by="PR Points", ascending=False)
