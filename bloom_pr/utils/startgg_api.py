import os
import requests
from dotenv import load_dotenv
from utils.character_mapping import get_character_name

load_dotenv()
API_KEY = os.getenv("STARTGG_API_KEY")
GRAPHQL_URL = "https://api.start.gg/gql/alpha"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def graphql_query(query, variables):
    response = requests.post(GRAPHQL_URL, json={"query": query, "variables": variables}, headers=HEADERS)
    data = response.json()
    if "errors" in data:
        raise ValueError("Erreur API StartGG : " + str(data["errors"]))
    return data

def get_phase_groups(slug):
    query = """
    query GetPhaseGroups($slug: String!) {
      tournament(slug: $slug) {
        name
        events {
          id
          name
          videogame { name }
          phaseGroups {
            id
          }
        }
      }
    }
    """
    data = graphql_query(query, {"slug": slug})
    tournament = data["data"]["tournament"]
    event = next(
        (e for e in tournament["events"]
         if e["videogame"]["name"].lower() == "super smash bros. ultimate"
         and "bracket ssbu" in e["name"].lower()),
        None
    )
    if not event:
        raise ValueError("Aucun événement Smash Ultimate trouvé dans ce tournoi.")

    phase_groups = event.get("phaseGroups") or []
    return tournament["name"], [pg["id"] for pg in phase_groups]

def get_sets_from_phase_group(pg_id):
    query = """
    query GetSets($phaseGroupId: ID!, $page: Int!) {
      phaseGroup(id: $phaseGroupId) {
        sets(page: $page, perPage: 50) {
          pageInfo { totalPages }
          nodes {
            id
            winnerId
            slots {
              entrant {
                id
                name
                participants {
                  gamerTag
                }
              }
            }
            games {
              selections {
                selectionType
                selectionValue
                entrant {
                  id
                }
              }
            }
          }
        }
      }
    }
    """
    sets = []
    page = 1
    while True:
        data = graphql_query(query, {"phaseGroupId": pg_id, "page": page})
        pg_data = data["data"]["phaseGroup"]["sets"]
        sets.extend(pg_data["nodes"])
        if page >= pg_data["pageInfo"]["totalPages"]:
            break
        page += 1
    return sets

def fetch_tournament_sets(slug):
    tournament_name, phase_group_ids = get_phase_groups(slug)
    all_sets = []
    for pg_id in phase_group_ids:
        try:
            sets = get_sets_from_phase_group(pg_id)
            all_sets.extend(sets)
        except Exception as e:
            print(f"Erreur lors de la récupération des sets pour le phaseGroup {pg_id} : {e}")
    return tournament_name, all_sets

def transform_to_local_format(set_nodes):
    players = {}
    matches = []

    for s in set_nodes:
        slots = s.get("slots")
        if not slots or len(slots) != 2:
            continue

        p1_slot, p2_slot = slots
        p1 = p1_slot.get("entrant")
        p2 = p2_slot.get("entrant")
        if not p1 or not p2:
            continue

        p1_id = str(p1.get("id"))
        p2_id = str(p2.get("id"))
        if not p1_id or not p2_id:
            continue

        players[p1_id] = {"id": p1_id, "tag": p1.get("name", "Unknown")}
        players[p2_id] = {"id": p2_id, "tag": p2.get("name", "Unknown")}

        winner_id = str(s.get("winnerId"))
        p1_win = (p1_id == winner_id)

        p1_char = "?"
        p2_char = "?"

        for game in s.get("games") or []:
            for sel in game.get("selections") or []:
                if sel.get("selectionType") == "CHARACTER":
                    eid = str(sel["entrant"].get("id")) if sel.get("entrant") else None
                    if eid == p1_id:
                        p1_char = get_character_name(sel.get("selectionValue"))
                    elif eid == p2_id:
                        p2_char = get_character_name(sel.get("selectionValue"))

        matches.append({
            "p1_id": p1_id,
            "p2_id": p2_id,
            "p1_character": p1_char,
            "p2_character": p2_char,
            "p1_win": p1_win
        })

    return list(players.values()), matches
