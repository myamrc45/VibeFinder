import streamlit as st
from navbar import show_navbar
from theme import apply_theme

st.set_page_config(
    page_title="Discover",
    layout="wide"
)
show_navbar()

apply_theme()   

st.title("Discover")
st.write("Explore different mood playlists.")

if st.button("😊 Happy"):
    st.switch_page("pages/Happy.py")

if st.button("☁️ Sad"):
    st.switch_page("pages/Sad.py")

if st.button("😌 Chill"):
    st.switch_page("pages/Chill.py")

if st.button("⚡ Energetic"):
    st.switch_page("pages/Energetic.py")

if st.button("💜 Romantic"):
    st.switch_page("pages/Romantic.py")

if st.button("😡 Angry"):
    st.switch_page("pages/Angry.py")