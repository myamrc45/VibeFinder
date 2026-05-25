import streamlit as st
import pandas as pd
import requests
from navbar import show_navbar
import joblib   
import base64
import streamlit.components.v1 as components
import random
import spotify_helpers  
from theme import apply_theme

#loading ML model       

model = joblib.load("mood_model.pkl")   


st.set_page_config(
    page_title="Romantic Playlist",
    layout="wide"
)

show_navbar()

apply_theme()       
st.title("Romantic Playlist")

st.write("""
Love songs and soft vibes for date nights and romance.
""")

if st.button("🔄 Refresh Playlist"):
    st.rerun()

# AI mood prediction based on song features 
prediction_data = [[
    0.68,   # danceability
    0.55,   # energy
    -6.0,   # loudness
    0.04,   # speechiness
    0.22,   # acousticness
    0.01,   # instrumentalness
    0.10,   # liveness
    0.88,   # valence
    105
]]

predicted_mood = model.predict(prediction_data)[0]

st.write("AI Selected Mood:", predicted_mood)

user_features = {
    "danceability": 0.68,
    "energy": 0.55,
    "loudness": -6.0,
    "speechiness": 0.04,
    "acousticness": 0.22,
    "instrumentalness": 0.01,
    "liveness": 0.10,
    "valence": 0.88,
    "tempo": 105
}

songs = spotify_helpers.get_similar_songs(
    predicted_mood,
    user_features,
    limit=10,
    genre_keywords=[
        "r-n-b",
        "love",
        "soul",
        "slow",
        "neo-soul",
        "romance",
        "jazz",
        "ballad"
    ]
)

st.subheader("🎧 Recommended Songs")

for index, row in songs.iterrows():

    if "track_id" in row:
        spotify_link = "https://open.spotify.com/track/" + str(row["track_id"])

        spotify_helpers.show_spotify_embed(spotify_link)

    else:
        st.warning(f"Missing Spotify track ID for: {row['track_name']}")