import streamlit as st
import pandas as pd
import os
from navbar import show_navbar
from theme import apply_theme

st.set_page_config(
    page_title="Profile",
    layout="wide"
)

show_navbar()
apply_theme()

st.title("👤 Profile")

st.subheader("Welcome back, Vibe Finder User")

col1, col2 = st.columns(2)

saved_playlists_file = "saved_playlists.csv"
saved_songs_file = "saved_songs.csv"

playlist_count = 0
song_count = 0
favorite_mood = "None yet"

if os.path.exists(saved_playlists_file):

    playlists_df = pd.read_csv(saved_playlists_file)

    playlist_count = playlists_df["mood"].nunique()

    if "mood" in playlists_df.columns and len(playlists_df) > 0:
        favorite_mood = playlists_df["mood"].mode()[0]  

with col1:
    st.metric("Saved Playlists", playlist_count)

with col2:
    st.metric("Top Mood", favorite_mood)

st.divider()

st.subheader("🎧 Your Music Identity")

st.write(f"""
You have saved **{playlist_count} playlists** so far.

Your most common mood is **{favorite_mood}**.
""")

if st.button("Go to Library", use_container_width=True):
    st.switch_page("pages/Playlist_History.py")