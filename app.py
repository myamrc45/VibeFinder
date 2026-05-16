import streamlit as st
import pandas as pd
import requests
from navbar import show_navbar
import joblib

LASTFM_API_KEY = "53a5c43985e65eacab28d9336a49f81c"

# Loading data
df = pd.read_csv("spotify_tracks.csv")

# testing to see if data loads correctly
# st.write(df.head())

# loading model

model = joblib.load("mood_model.pkl")

# dropping nulls
df = df.drop(columns=["Unnamed: 0"])

# Page setup
st.set_page_config(
    page_title="Vibe Finder",
    page_icon="🎵",
    layout="centered"
)

show_navbar()

st.write("Find music based on your mood or vibe.")

# filter by genre 
genre_options = ["All"] + sorted(df["track_genre"].dropna().unique().tolist())

selected_genre = st.selectbox(
    "Filter by genre:",
    genre_options
)


def get_mood_from_text(vibe_text):
    vibe_text = vibe_text.lower()

    if "happy" in vibe_text or "fun" in vibe_text or "excited" in vibe_text:
        return "Happy"

    elif "sad" in vibe_text or "cry" in vibe_text or "lonely" in vibe_text:
        return "Sad"

    elif "chill" in vibe_text or "relax" in vibe_text or "calm" in vibe_text:
        return "Chill"

    elif "love" in vibe_text or "romantic" in vibe_text or "date" in vibe_text:
        return "Romantic"

    elif "energy" in vibe_text or "workout" in vibe_text or "hype" in vibe_text:
        return "Energetic"

    elif "angry" in vibe_text or "mad" in vibe_text or "rage" in vibe_text:
        return "Angry"

    else:
        return "Chill"

# song recommendation via AI

def recommend_songs(mood, data):
    filtered = data[data["mood"] == mood]

    if len(filtered) < 10:
        return filtered

    return filtered.sample(10)


def get_lastfm_tracks(tag):
    url = "https://ws.audioscrobbler.com/2.0/"

    params = {
        "method": "tag.gettoptracks",
        "tag": tag.lower(),
        "api_key": LASTFM_API_KEY,
        "format": "json",
        "limit": 10
    }

    response = requests.get(url, params=params)
    data = response.json()

    tracks = data["tracks"]["track"]

    song_list = []

    for track in tracks:
        song_list.append({
            "Song": track["name"],
            "Artist": track["artist"]["name"],
            "Last.fm Link": track["url"]
        })

    return pd.DataFrame(song_list)


st.markdown("---")

st.subheader("Choose a Mood")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("😊 Happy"):
        st.switch_page("pages/Happy.py")

with col2:
    if st.button("☁️ Sad"):
        st.switch_page("pages/Sad.py")

with col3:
    if st.button("😌 Chill"):
        st.switch_page("pages/Chill.py")

col4, col5, col6 = st.columns(3) 

with col4:
    if st.button("💜 Romantic"):
        st.switch_page("pages/Romantic.py")

with col5:
    if st.button("⚡ Energetic"):
        st.switch_page("pages/Energetic.py")

with col6:
    if st.button("😡 Angry"):
        st.switch_page("pages/Angry.py")
        
vibe_text = st.text_input(
    "Describe your vibe:",
    placeholder="Late night drive in the rain"
)

if vibe_text:
    mood = get_mood_from_text(vibe_text)

    st.success(f"Detected Mood: {mood}")

    st.subheader("🎧 Dataset Recommendations")
    csv_tracks = recommend_songs(mood, df)
    st.dataframe(csv_tracks)

    st.subheader("🌍 Last.fm API Recommendations")
    api_tracks = get_lastfm_tracks(mood)
    st.dataframe(api_tracks)

else:
    st.info("Type a vibe above or choose a mood playlist from the choices above.")   




st.divider()

st.subheader("AI Mood Quiz")

energy_quiz = st.radio(
    "How energetic do you feel?",
    [1,2,3,4,5,6,7,8,9,10],
    horizontal=True
)

dance_quiz = st.radio(
    "How upbeat is your mood?",
    [1,2,3,4,5,6,7,8,9,10],
    horizontal=True
)

acoustic_quiz = st.radio(
    "How relaxed are you feeling?",
    [1,2,3,4,5,6,7,8,9,10],
    horizontal=True
)

valence_quiz = st.radio(
    "How positive is your mood?",
    [1,2,3,4,5,6,7,8,9,10],
    horizontal=True
)

tempo_quiz = st.radio(
    "How active do you feel?",
    [1,2,3,4,5,6,7,8,9,10],
    horizontal=True
)

# AI prediction based on quiz answers

if st.button("Predict Mood"):

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

    st.write("Predicted Mood:", predicted_mood)

    tracks = get_lastfm_tracks(predicted_mood)



    st.dataframe(tracks)
    if predicted_mood == "Happy":
        st.switch_page("pages/Happy.py")

    elif predicted_mood == "Sad":
        st.switch_page("pages/Sad.py")

    elif predicted_mood == "Chill":
        st.switch_page("pages/Chill.py")

    elif predicted_mood == "Romantic":
        st.switch_page("pages/Romantic.py")

    elif predicted_mood == "Energetic":
        st.switch_page("pages/Energetic.py")

    elif predicted_mood == "Angry":
        st.switch_page("pages/Angry.py")