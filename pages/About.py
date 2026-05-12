import streamlit as st
from navbar import show_navbar

st.set_page_config(page_title="About", page_icon="ℹ️")

show_navbar()

st.title("ℹ️ About Vibe Finder")
st.write("""
Vibe Finder is a music recommendation app that helps users find songs based on their mood.

The app uses mood categories, a dataset, and the Last.fm API to recommend songs.
""")