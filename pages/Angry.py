import streamlit as st
import pandas as pd
from navbar import show_navbar
import joblib   
import streamlit.components.v1 as components
import spotify_helpers   


#loading ML model       

model = joblib.load("mood_model.pkl")   


st.set_page_config(page_title="Angry Playlist", page_icon="😡")

show_navbar()


st.title("😡 Angry Playlist")

st.write("""
Aggressive and intense songs to match strong emotions.
""")

if st.button("🔄 Refresh Playlist"):
    st.rerun()

# AI mood prediction based on song features 

prediction_data = [[
    0.18,   # danceability
    1.00,   # energy
    -1.0,   # loudness
    0.15,   # speechiness
    0.00,   # acousticness
    0.00,   # instrumentalness
    0.40,   # liveness
    0.02,   # valence
    185     # tempo
]]

predicted_mood = model.predict(prediction_data)[0]

st.write("AI Selected Mood:", predicted_mood)

user_features = {
    "danceability": 0.18,
    "energy": 1.00,
    "loudness": -1.0,
    "speechiness": 0.15,
    "acousticness": 0.00,
    "instrumentalness": 0.00,
    "liveness": 0.40,
    "valence": 0.02,
    "tempo": 185
}

songs = spotify_helpers.get_similar_songs(
    predicted_mood,
    user_features,
    limit=10,
    genre_keywords=[
        "rock",
        "metal",
        "punk",
        "hardcore",
        "hip-hop",
        "rap"
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