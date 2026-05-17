import streamlit as st
import pandas as pd
import requests
from navbar import show_navbar
import joblib   
import base64
import streamlit.components.v1 as components
import random   


#loading ML model       

model = joblib.load("mood_model.pkl")   


st.set_page_config(page_title="Angry Playlist", page_icon="😡")

show_navbar()

# spotify credentials from secrets.toml

SPOTIFY_CLIENT_ID = st.secrets["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = st.secrets["SPOTIFY_CLIENT_SECRET"]

# spotify api   

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


def get_spotify_tracks(mood):
    token = get_spotify_token()

    url = "https://api.spotify.com/v1/search"

    headers = {
        "Authorization": "Bearer " + token
    }

    params = {
        "q": mood + " songs",
        "type": "track",
        "limit": 10,
        "offset": random.randint(0, 90)
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

    random.shuffle(song_list)

    return pd.DataFrame(song_list)


def show_spotify_embed(track_url):
    embed_url = track_url.replace(
        "https://open.spotify.com/track/",
        "https://open.spotify.com/embed/track/"
    )

    components.iframe(embed_url, height=152)

st.title("😡 Angry Playlist")

st.write("""
Aggressive and intense songs to match strong emotions.
""")

# AI mood prediction based on song features 

prediction_data = [[
    0.40,   # danceability
    0.98,   # energy
    -2.0,   # loudness
    0.18,   # speechiness
    0.02,   # acousticness
    0.0,    # instrumentalness
    0.35,   # liveness
    0.08,   # valence
    175     # tempo
]]

predicted_mood = model.predict(prediction_data)[0]

st.write("AI Selected Mood:", predicted_mood)

angry_songs_spotify = get_spotify_tracks(predicted_mood.lower())


df = pd.read_csv("spotify_tracks.csv")

st.subheader("🎧 Recommended Songs")

for index, row in angry_songs_spotify.iterrows():
    st.subheader(row["Song"])
    st.write("Artist:", row["Artist"])
    st.write("Album:", row["Album"])
    show_spotify_embed(row["Spotify Link"])

st.warning("Let the music release the stress 🖤")