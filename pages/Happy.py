import streamlit as st
import pandas as pd
import requests
from navbar import show_navbar
import joblib   

#loading ML model       

model = joblib.load("mood_model.pkl")   


st.set_page_config(page_title="Happy Playlist", page_icon="😊")

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

st.title("😊 Happy Playlist")

st.write("""
Songs to boost your mood and keep the good vibes going.
""")

# AI mood prediction based on song features 
prediction_data = [[
    0.85,
    0.75,
    -6.0,
    0.05,
    0.20,
    0.0,
    0.15,
    0.90,
    120
]]

predicted_mood = model.predict(prediction_data)[0]
st.write("AI Selected Mood:", predicted_mood)

happy_songs_lastfm = get_lastfm_tracks(predicted_mood.lower())

df = pd.read_csv("spotify_tracks.csv")

st.subheader("🎧 Recommended Songs")

for index, row in happy_songs_lastfm.iterrows():

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

st.success("Enjoy your happy vibes 🎉")