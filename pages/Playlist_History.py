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

                spotify_data = spotify_helpers.search_spotify_track(
                    row["song"],
                    row["artist"]
                )

                if spotify_data:

                    spotify_helpers.show_spotify_embed(
                        spotify_data["link"]
                    )

                else:
                    st.warning(
                        f"Could not find {row['song']} on Spotify."
                    )