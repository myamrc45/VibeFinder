import streamlit as st
import pandas as pd
import requests

LASTFM_API_KEY = "53a5c43985e65eacab28d9336a49f81c"

def get_lastfm_tracks(mood):
    url = "http://ws.audioscrobbler.com/2.0/"

    params = {
        "method": "tag.gettoptracks",
        "tag": mood.lower(),
        "api_key": LASTFM_API_KEY,
        "format": "json",
        "limit": 20
    }

    response = requests.get(url, params=params)
    data = response.json()

    return data["tracks"]["track"]

# Loading data
df = pd.read_csv("spotify_tracks.csv")

# testing to see if data loads correctly
# st.write(df.head())


# dropping nulls
df = df.drop(columns=["Unnamed: 0"])

# Reccomendations based on mood via data set
def recommend_songs(mood, data):
    if mood == "Happy":
        filtered = data[(data["energy"] > 0.6) & (data["danceability"] > 0.6)]

    elif mood == "Sad":
        filtered = data[(data["energy"] < 0.4) & (data["danceability"] < 0.5)]

    elif mood == "Energetic":
        filtered = data[(data["energy"] > 0.75) & (data["danceability"] > 0.65)]

    elif mood == "Chill":
        filtered = data[(data["energy"] < 0.5) & (data["acousticness"] > 0.4)]

    elif mood == "Romantic":
        filtered = data[(data["energy"] > 0.3) & (data["energy"] < 0.7) & (data["danceability"] > 0.4)]

    else:
        filtered = data

    return filtered.sample(500)

# Mood from user input 
def get_mood_from_text(vibe_text):
    vibe_text = vibe_text.lower()

    if "happy" in vibe_text or "fun" in vibe_text or "party" in vibe_text:
        return "Happy"

    elif "sad" in vibe_text or "cry" in vibe_text or "heartbreak" in vibe_text or "rain" in vibe_text:
        return "Sad"

    elif "energy" in vibe_text or "gym" in vibe_text or "hype" in vibe_text or "workout" in vibe_text:
        return "Energetic"

    elif "chill" in vibe_text or "relax" in vibe_text or "calm" in vibe_text or "late night" in vibe_text:
        return "Chill"

    elif "love" in vibe_text or "romantic" in vibe_text or "date" in vibe_text:
        return "Romantic"

    else:
        return "Chill"



# Page setup
st.set_page_config(
    page_title="Vibe Finder",
    page_icon="🎵",
    layout="centered"
)

# Title
st.title("🎵 Vibe Finder")
st.write("Find music based on your mood or vibe.")

# Mood section
st.subheader("How are you feeling today?")

if "selected_mood" not in st.session_state:
    st.session_state.selected_mood = None

# Create columns
col1, col2, col3, col4, col5 = st.columns(5)

selected_mood = None

with col1:
    if st.button("😌 Chill"):
        st.session_state.selected_mood = "Chill"

with col2:
    if st.button("😁 Happy"):
        st.session_state.selected_mood = "Happy"

with col3:
    if st.button("🌧️ Sad"):
        st.session_state.selected_mood = "Sad"

with col4:
    if st.button("⚡ Energetic"):
        st.session_state.selected_mood = "Energetic"

with col5:
    if st.button("💜 Romantic"):
        st.session_state.selected_mood = "Romantic"
# Text input
vibe_text = st.text_input(
    "Or describe your vibe:",
    placeholder="Late night drive in the rain"
)

# filter by genre 
genre_options = ["All"] + sorted(df["track_genre"].dropna().unique().tolist())

selected_genre = st.selectbox(
    "Filter by genre:",
    genre_options
)


# Output
mood = st.session_state.selected_mood

# If user types a vibe, use that instead
if vibe_text:
    mood = get_mood_from_text(vibe_text)

if mood:
    st.success(f"Vibe detected: {mood}")
    api_tracks = get_lastfm_tracks(mood)

    results = recommend_songs(mood, df)

    if selected_genre != "All":
        results = results[results["track_genre"] == selected_genre]


    st.subheader("Dataset Recommendations")

    if results.empty:
        st.warning("No songs found for this mood and genre. Try another genre.")
    else:
        for index, row in results.iterrows():
            st.write(f"🎧 **{row['track_name']}** by {row['artists']}")
            st.write(f"Genre: {row['track_genre']}")
            st.write(f"Popularity: {row['popularity']}")
            st.write("---")