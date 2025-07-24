import streamlit as st
from db.init_db import init_db
init_db()
st.set_page_config(
    page_title="Smash PR App",
    layout="wide"
)
import sqlite3
conn = sqlite3.connect("smash_pr.db")
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(c.fetchall())


st.title("🏆 Accueil – Smash Ultimate PR")
st.markdown("""
Bienvenue dans l'application de Power Ranking Smash Bros Ultimate !

Utilise le menu de gauche pour :
- Importer un tournoi
- Voir les statistiques d'un joueur
- Suivre les Elos par personnage
""")
