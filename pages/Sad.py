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


st.set_page_config(page_title="Sad Playlist", page_icon="😢")

show_navbar()

st.title("😢 Sad Playlist")

st.write("""
Songs for emotional moments, reflection, and comfort.
""")

if st.button("🔄 Refresh Playlist"):
    st.rerun()

# AI mood prediction based on song features 
prediction_data = [[
    0.32,   # danceability
    0.22,   # energy
    -12.0,  # loudness
    0.04,   # speechiness
    0.72,   # acousticness
    0.03,   # instrumentalness
    0.10,   # liveness
    0.10,   # valence
    68      # tempo
]]

predicted_mood = model.predict(prediction_data)[0]

st.write("AI Selected Mood:", predicted_mood)

user_features = {
    "danceability": 0.32,
    "energy": 0.22,
    "loudness": -12.0,
    "speechiness": 0.04,
    "acousticness": 0.72,
    "instrumentalness": 0.03,
    "liveness": 0.10,
    "valence": 0.10,
    "tempo": 68
}

songs = spotify_helpers.get_similar_songs(
    predicted_mood,
    user_features,
    limit=10,
    genre_keywords=[
        "sad",
        "acoustic",
        "piano",
        "ballad",
        "indie",
        "singer-songwriter",
        "r-n-b",
        "emotional"
    ]
)

st.subheader("🎧 Recommended Songs")

for index, row in songs.iterrows():

    song_name = row["track_name"]
    artist = row["artists"]

    spotify_data = spotify_helpers.search_spotify_track(
        song_name,
        artist
    )

    with st.container(border=True):

        if spotify_data:
            st.image(spotify_data["cover"], use_container_width=True)

        st.subheader(song_name)
        st.caption(f"Artist: {artist}")

        st.write("Mood-based AI recommendation")

        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            st.caption("10 songs")

        with col2:
            st.caption("AI Pick")

        if spotify_data:
            spotify_helpers.show_spotify_embed(
                spotify_data["link"]
            )

    st.write("")