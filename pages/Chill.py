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
    page_title="Chill Playlist",
    layout="wide"
)

show_navbar()

apply_theme()   

st.title("Chill Playlist")

st.write("""
Relaxing songs for studying, resting, or peaceful vibes.
""")

if st.button("🔄 Refresh Playlist"):
    st.rerun()

# AI mood prediction based on song features 
prediction_data = [[
    0.55,   # danceability
    0.45,   # energy
    -11.0,  # loudness
    0.04,   # speechiness
    0.80,   # acousticness
    0.15,   # instrumentalness
    0.10,   # liveness
    0.55,   # valence
    90      # tempo    
]]

predicted_mood = model.predict(prediction_data)[0]

st.write("AI Selected Mood:", predicted_mood)

user_features = {
    "danceability": 0.55,
    "energy": 0.45,
    "loudness": -11.0,
    "speechiness": 0.04,
    "acousticness": 0.80,
    "instrumentalness": 0.15,
    "liveness": 0.10,
    "valence": 0.55,
    "tempo": 90
}

songs = spotify_helpers.get_similar_songs(
    predicted_mood,
    user_features,
    limit=10,
    genre_keywords=[
        "chill",
        "ambient",
        "acoustic",
        "lo-fi",
        "jazz",
        "study",
        "piano",
        "indie"
    ]
)

st.subheader("🎧 Recommended Songs")

for index, row in songs.iterrows():

    if "track_id" in row:
        spotify_link = "https://open.spotify.com/track/" + str(row["track_id"])

        spotify_helpers.show_spotify_embed(spotify_link)

    else:
        st.warning(f"Missing Spotify track ID for: {row['track_name']}")