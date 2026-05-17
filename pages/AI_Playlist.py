import streamlit as st
import pandas as pd
from navbar import show_navbar
import joblib
import streamlit.components.v1 as components
import spotify_helpers

st.set_page_config(page_title="AI Playlist", page_icon="🎧")

# loading ML model
model = joblib.load("mood_model.pkl")   

show_navbar()   


st.title("🎧 AI Playlist")
st.write("Answer the quiz and let AI recommend songs based on your music vibe.")


options = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

energy_quiz = st.radio(
    "How much energy do you want?",
    options,
    horizontal=True
)

dance_quiz = st.radio(
    "How danceable should it feel?",
    options,
    horizontal=True
)

acoustic_quiz = st.radio(
    "How soft or acoustic should it feel?",
    options,
    horizontal=True
)

valence_quiz = st.radio(
    "How positive should the vibe feel?",
    options,
    horizontal=True
)

tempo_quiz = st.radio(
    "How fast should the music feel?",
    options,
    horizontal=True
)


if st.button("Generate AI Playlist"):

    energy = energy_quiz / 10
    danceability = dance_quiz / 10
    acousticness = acoustic_quiz / 10
    valence = valence_quiz / 10
    tempo = tempo_quiz * 20

    prediction_data = [[
        danceability,
        energy,
        -10.0,
        0.05,
        acousticness,
        0.0,
        0.1,
        valence,
        tempo
    ]]

    predicted_mood = model.predict(prediction_data)[0]

    user_features = {
        "danceability": danceability,
        "energy": energy,
        "loudness": -10.0,
        "speechiness": 0.05,
        "acousticness": acousticness,
        "instrumentalness": 0.0,
        "liveness": 0.1,
        "valence": valence,
        "tempo": tempo
    }

    st.success(f"AI predicted your mood: {predicted_mood}")

    songs = spotify_helpers.get_similar_songs(predicted_mood, user_features, limit=10)

    for index, row in songs.iterrows():
        song_name = row["track_name"] if "track_name" in row else row["name"]
        artist = row["artists"] if "artists" in row else row["artist_name"]

        st.subheader(song_name)
        st.write("Artist:", artist)

        spotify_link = spotify_helpers.search_spotify_track(song_name, artist)

        if spotify_link:
            spotify_helpers.show_spotify_embed(spotify_link)
        else:
            st.warning("Could not find this track on Spotify.")