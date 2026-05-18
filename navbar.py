import streamlit as st

def show_navbar():

    st.title("🎵 Vibe Finder")

    st.write("")

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        if st.button("Home", use_container_width=True):
            st.switch_page("app.py")

    with col2:
        if st.button("Discover", use_container_width=True):
            st.switch_page("pages/Discover.py")

    with col3:
        if st.button("AI Playlist", use_container_width=True):
            st.switch_page("pages/AI_Playlist.py")

    with col4:
        if st.button("Library", use_container_width=True):
            st.switch_page("pages/Playlist_History.py")

    with col5:
        if st.button("About", use_container_width=True):
            st.switch_page("pages/About.py")

    with col6:
        if st.button("👤", use_container_width=True):
            st.switch_page("pages/Profile.py")

    st.divider()
