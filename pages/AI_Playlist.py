import streamlit as st
from navbar import show_navbar

st.set_page_config(page_title="AI Playlist", page_icon="🤖")

show_navbar()

st.title("🤖 AI Playlist")
st.write("Describe your vibe and get music recommendations.")

vibe_text = st.text_input(
    "Describe your vibe:",
    placeholder="Late night drive in the rain"
)

if vibe_text:
    st.success(f"Generating playlist for: {vibe_text}")