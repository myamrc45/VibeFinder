import streamlit as st
from navbar import show_navbar

st.set_page_config(
    page_title="Profile",
    page_icon="👤",
    layout="centered"
)

show_navbar()

st.header("Profile")

st.image(
    "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
    width=120
)

st.subheader("Mya")

st.write("Welcome to your Vibe Finder profile.")

st.divider()

st.subheader("🎧 Favorite Genres")

genre1 = st.checkbox("R&B")
genre2 = st.checkbox("Pop")
genre3 = st.checkbox("Afrobeats")
genre4 = st.checkbox("Hip-Hop")
genre5 = st.checkbox("Chill")

st.divider()

st.subheader("💜 Favorite Moods")

mood = st.selectbox(
    "Choose your favorite mood:",
    ["Happy", "Sad", "Chill", "Romantic", "Energetic", "Angry"]
)

st.write(f"Your favorite mood is: **{mood}**")

st.divider()

st.subheader("🔥 Recently Visited")

st.write("😊 Happy Playlist")
st.write("😌 Chill Playlist")
st.write("💜 Romantic Playlist")