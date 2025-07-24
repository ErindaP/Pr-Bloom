import streamlit as st
from db.database import init_db
from logic.pr_calculator import compute_power_ranking
import pandas as pd
from utils.startgg_api import fetch_tournament_sets, transform_to_local_format
from logic.import_startgg_to_db import import_tournament


st.set_page_config(page_title="Smash PR", layout="wide")
st.title("🏆 Smash Bros Ultimate – Power Ranking")

# Init BDD
#init_db()

uploaded_file = st.file_uploader("Importer un bracket (JSON)", type=["json"])
if uploaded_file:
    from utils.bracket_parser import parse_bracket
    matches, players = parse_bracket(uploaded_file)

    st.success("Bracket importé avec succès.")
    pr_df = compute_power_ranking(matches, players)
    st.dataframe(pr_df)


with st.expander("Importer un tournoi depuis StartGG"):
    slug = st.text_input("Slug StartGG (ex: tournoi-smash-paris-3)")
    if st.button("Importer depuis StartGG"):
        try:
            tournament_name, raw_sets = fetch_tournament_sets(slug)
            players, matches = transform_to_local_format(raw_sets)
            st.success(f"{len(matches)} matchs importés depuis : {tournament_name}")
            pr_df = compute_power_ranking(matches, players)
            st.dataframe(pr_df)
        except ValueError as e:
            st.error(str(e))
    if st.button("Importer dans db"):
        try:
            name, match_count, player_count = import_tournament(slug)
            st.success(f"✅ {name} importé avec {match_count} matchs et {player_count} joueurs.")
        except Exception as e:
            st.error(f"Erreur : {e}")