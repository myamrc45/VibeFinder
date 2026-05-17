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


st.set_page_config(page_title="Happy Playlist", page_icon="😊")

show_navbar()


st.title("😊 Happy Playlist")

st.write("""
Songs to boost your mood and keep the good vibes going.
""")

if st.button("🔄 Refresh Playlist"):
    st.rerun()

# AI mood prediction based on song features 
prediction_data = [[
    0.72,   # danceability
    0.65,   # energy
    -5.0,   # loudness
    0.05,   # speechiness
    0.18,   # acousticness
    0.00,   # instrumentalness
    0.15,   # liveness
    0.98,   # valence
    112     # tempo
]]

predicted_mood = model.predict(prediction_data)[0]

st.write("AI Selected Mood:", predicted_mood)

user_features = {
    "danceability": 0.72,
    "energy": 0.65,
    "loudness": -5.0,
    "speechiness": 0.05,
    "acousticness": 0.18,
    "instrumentalness": 0.00,
    "liveness": 0.15,
    "valence": 0.98,
    "tempo": 112
}

songs = spotify_helpers.get_similar_songs(
    predicted_mood,
    user_features,
    limit=10,
    genre_keywords=[
        "pop",
        "dance",
        "happy",
        "funk",
        "disco",
        "party",
        "summer",
        "r-n-b"
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