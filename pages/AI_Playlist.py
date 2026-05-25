import streamlit as st
import pandas as pd
from navbar import show_navbar
import joblib
import streamlit.components.v1 as components
import spotify_helpers
import playlist_helpers
import time
from theme import apply_theme
from song_cards import show_song_embed

st.set_page_config(
    page_title="AI Playlist ",
    layout="wide"
)

# loading ML model
model = joblib.load("mood_model.pkl")   

show_navbar()   

apply_theme()

# AI recommendation function
def recommend_songs(df, mood, energy, dance, acoustic, valence, tempo, loudness, speechiness, liveness):
    df = df.copy()

    df["score"] = 0

    # mood match
    df.loc[df["mood"] == mood, "score"] += 5

    # compare audio features
    df["score"] += 10 - abs(df["energy"] - energy)
    df["score"] += 10 - abs(df["danceability"] - dance)
    df["score"] += 10 - abs(df["acousticness"] - acoustic)
    df["score"] += 10 - abs(df["valence"] - valence)
    df["score"] += 10 - abs(df["tempo"] - tempo)
    df["score"] += 10 - abs(df["loudness"] - loudness)
    df["score"] += 10 - abs(df["speechiness"] - speechiness)
    df["score"] += 10 - abs(df["liveness"] - liveness)

    df = df.sort_values(by="score", ascending=False)

    top_matches = df.head(50)

    if len(top_matches) > 10:
        return top_matches.sample(
            n=10,
            random_state=int(time.time())
        )

    return top_matches


st.title("AI Mood Quiz")
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
loudness_quiz = st.radio(
    "How loud/intense should the music feel?",
    options,
    horizontal=True
)

speechiness_quiz = st.radio(
    "How much talking or rapping should it have?",
    options,
    horizontal=True
)

liveness_quiz = st.radio(
    "How live or concert-like should it feel?",
    options,
    horizontal=True
)

if st.button("🔄 Refresh Playlist"):
        st.session_state["refresh_playlist"] = True
        st.rerun()  


generate_clicked = st.button("Generate AI Playlist")

if generate_clicked or st.session_state.get("refresh_playlist", False):

    st.session_state["refresh_playlist"] = False


    energy = energy_quiz / 10
    danceability = dance_quiz / 10
    acousticness = acoustic_quiz / 10
    valence = valence_quiz / 10
    tempo = tempo_quiz * 20
    loudness = loudness_quiz * -6
    speechiness = speechiness_quiz / 10
    liveness = liveness_quiz / 10

    prediction_data = [[
    danceability,
    energy,
    loudness,
    speechiness,
    acousticness,
    0.0,    # instrumentalness is always 0 for user input since we want songs with vocals
    liveness,
    valence,
    tempo
]]

    predicted_mood = model.predict(prediction_data)[0]

    user_features = {
    "danceability": danceability,
    "energy": energy,
    "loudness": loudness,
    "speechiness": speechiness,
    "acousticness": acousticness,
    "instrumentalness": 0.0,
    "liveness": liveness,
    "valence": valence,
    "tempo": tempo}

    st.success(f"AI predicted your mood: {predicted_mood}")

    songs_df = spotify_helpers.get_similar_songs(
        predicted_mood,
        user_features,
        limit=100
    )

    songs = recommend_songs(
    songs_df,
    predicted_mood,
    energy,
    danceability,
    acousticness,
    valence,
    tempo,
    loudness,
    speechiness,
    liveness,
)

    st.session_state["last_playlist"] = songs
    st.session_state["last_mood"] = predicted_mood


    for index, row in songs.iterrows():

        if "track_id" in row:
            spotify_link = "https://open.spotify.com/track/" + str(row["track_id"])

            spotify_helpers.show_spotify_embed(spotify_link)

        else:
            st.warning(f"Missing Spotify track ID for: {row['song']}")

if "last_playlist" in st.session_state:

    if st.button("Save This Playlist", key="save_ai_playlist"):

        playlist_helpers.save_playlist(
            st.session_state["last_mood"],
            st.session_state["last_playlist"]
        )

        st.success("Playlist saved!")




    