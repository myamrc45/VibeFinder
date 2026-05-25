import streamlit as st
import playlist_helpers
import spotify_helpers
from navbar import show_navbar
from theme import apply_theme


st.set_page_config(
    page_title="Playlist History",
    layout="wide"
)

show_navbar()

apply_theme()   

st.title("Playlist Library")
st.write("Your saved playlists organized by mood.")

history = playlist_helpers.load_playlist_history()

if len(history) == 0:
    st.info("No playlists saved yet.")

else:
    moods = history["mood"].unique()

    for mood in moods:

        mood_songs = history[history["mood"] == mood]

        with st.expander(
            f"{mood} Playlist — {len(mood_songs)} saved songs",
            expanded=False
        ):

            for index, row in mood_songs.iterrows():

                if "track_id" in row:
                    spotify_link = "https://open.spotify.com/track/" + str(row["track_id"])

                    spotify_helpers.show_spotify_embed(spotify_link)

            else:
                st.warning(f"Missing Spotify track ID for: {row['song']}")  