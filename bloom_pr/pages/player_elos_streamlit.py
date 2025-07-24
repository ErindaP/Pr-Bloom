import streamlit as st
import pandas as pd
from db.character_elos import get_elos_by_player
from db.database import get_connection
from utils.character_mapping import get_character_name

st.title("🎮 Statistiques par joueur et personnages")

# Charger les joueurs depuis la base
def get_all_players():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT DISTINCT id, tag FROM players ORDER BY tag ASC")
    players = c.fetchall()
    conn.close()
    return players

players = get_all_players()
if not players:
    st.info("Aucun joueur trouvé. Veuillez importer un tournoi.")
else:
    tag_to_id = {tag: pid for pid, tag in players}
    selected_tag = st.selectbox("Choisis un joueur", list(tag_to_id.keys()))
    player_id = tag_to_id[selected_tag]

    elos = get_elos_by_player(player_id)
    if not elos:
        st.warning("Ce joueur n'a pas encore d'Elo enregistré pour ses personnages.")
    else:
        df = pd.DataFrame([
            {
                "Personnage": get_character_name(char),
                "Elo": elo
            }
            for char, elo in elos.items()
        ])
        df = df.sort_values(by="Elo", ascending=False)
        st.subheader(f"\u2b50 Elo par personnage pour {selected_tag}")
        st.dataframe(df, use_container_width=True)
