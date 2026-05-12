import streamlit as st
import pandas as pd
import requests
from navbar import show_navbar

st.set_page_config(page_title="Energetic Playlist", page_icon="⚡")

show_navbar()

LASTFM_API_KEY = "53a5c43985e65eacab28d9336a49f81c"

def get_lastfm_tracks(tag):

    url = "https://ws.audioscrobbler.com/2.0/"

    params = {
        "method": "tag.gettoptracks",
        "tag": tag,
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

st.title("⚡ Energetic Playlist")

st.write("""
High-energy songs for workouts, motivation, and hype moments.
""")

energetic_songs_lastfm = get_lastfm_tracks("energetic") 

df = pd.read_csv("spotify_tracks.csv")

st.subheader("🎧 Recommended Songs")

for index, row in energetic_songs_lastfm.iterrows():

    st.markdown(
        f"""
        <div style="
            background-color: #f7f3ff;
            padding: 18px;
            border-radius: 15px;
            margin-bottom: 15px;
            border-left: 6px solid #7B61FF;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
        ">
            <h4 style="margin-bottom: 5px;">🎵 {row['Song']}</h4>
            <p style="margin: 0;">Artist: <b>{row['Artist']}</b></p>
            <a href="{row['Last.fm Link']}" target="_blank">Open on Last.fm</a>
        </div>
        """,
        unsafe_allow_html=True
    )

st.success("Get energized 🔥")