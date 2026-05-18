import streamlit as st
import playlist_helpers
from navbar import show_navbar


st.set_page_config(
    page_title="Playlist History",
    page_icon="📚"
)

show_navbar()

st.title("📚 Playlist History")

history = playlist_helpers.load_playlist_history()

if len(history) > 0:
    st.dataframe(history)
else:
    st.info("No playlists saved yet.")