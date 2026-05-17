import streamlit as st
import pandas as pd
import requests
from navbar import show_navbar
import joblib   
import base64
import streamlit.components.v1 as components
import random
import spotify_helpers  

#loading ML model
model = joblib.load("mood_model.pkl")   

st.set_page_config(page_title="Energetic Playlist", page_icon="⚡")

show_navbar()


st.title("⚡ Energetic Playlist")

st.write("""
High-energy songs for workouts, motivation, and hype moments.
""")

if st.button("🔄 Refresh Playlist"):
    st.rerun()

# AI mood prediction based on song features 
prediction_data = [[
    0.82,   # danceability
    0.95,   # energy
    -3.0,   # loudness
    0.10,   # speechiness
    0.05,   # acousticness
    0.00,   # instrumentalness
    0.25,   # liveness
    0.88,   # valence
    150     # tempo
]]

predicted_mood = model.predict(prediction_data)[0]

st.write("AI Selected Mood:", predicted_mood)

user_features = {
    "danceability": 0.82,
    "energy": 0.95,
    "loudness": -3.0,
    "speechiness": 0.10,
    "acousticness": 0.05,
    "instrumentalness": 0.00,
    "liveness": 0.25,
    "valence": 0.88,
    "tempo": 150
}

songs = spotify_helpers.get_similar_songs(
    predicted_mood,
    user_features,
    limit=10,
    genre_keywords=[
        "dance",
        "edm",
        "electronic",
        "house",
        "pop",
        "hip-hop",
        "workout",
        "party"
    ]
)

st.subheader("🎧 Recommended Songs")

for index, row in songs.iterrows():

    song_name = row["track_name"]
    artist = row["artists"]

    st.subheader(song_name)

    st.write("Artist:", artist)

    spotify_link = spotify_helpers.search_spotify_track(
        song_name,
        artist
    )

    if spotify_link:

        spotify_helpers.show_spotify_embed(
            spotify_link
        )

        st.markdown(
            f"[Open in Spotify]({spotify_link})"
        )

    else:
        st.warning(
            "Could not find this track on Spotify."
        )