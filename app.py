import streamlit as st
import pandas as pd
import requests
from navbar import show_navbar
import joblib
import base64
import streamlit.components.v1 as components

# my spotify credentials from secrets.toml

SPOTIFY_CLIENT_ID = st.secrets["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = st.secrets["SPOTIFY_CLIENT_SECRET"]

# LASTFM_API_KEY = "53a5c43985e65eacab28d9336a49f81c"

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


def get_spotify_token():
    auth_string = SPOTIFY_CLIENT_ID + ":" + SPOTIFY_CLIENT_SECRET
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post(url, headers=headers, data=data)
    return response.json()["access_token"]

# spotify API recommendation based on mood  

def get_spotify_tracks(mood):
    token = get_spotify_token()

    url = "https://api.spotify.com/v1/search"

    headers = {
        "Authorization": "Bearer " + token
    }

    params = {
        "q": mood + " songs",
        "type": "track",
        "limit": 10
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    song_list = []

    for item in data["tracks"]["items"]:
        song_list.append({
            "Song": item["name"],
            "Artist": item["artists"][0]["name"],
            "Album": item["album"]["name"],
            "Spotify Link": item["external_urls"]["spotify"],
            "Album Cover": item["album"]["images"][0]["url"]
        })

    return pd.DataFrame(song_list)


def show_spotify_embed(track_url):
    embed_url = track_url.replace(
        "https://open.spotify.com/track/",
        "https://open.spotify.com/embed/track/"
    )

    components.iframe(embed_url, height=152)

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

    st.subheader("🌍 Spotify API Recommendations")
    api_tracks = get_spotify_tracks(mood)
    st.dataframe(api_tracks)

else:
    st.info("Type a vibe above or choose a mood playlist from the choices above.")   