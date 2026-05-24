import streamlit.components.v1 as components

def show_song_embed(track_url):
    embed_url = track_url.replace(
        "https://open.spotify.com/track/",
        "https://open.spotify.com/embed/track/"
    )

    components.iframe(
        embed_url,
        height=152,
        scrolling=False
    )