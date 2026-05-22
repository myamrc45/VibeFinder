import pandas as pd
import requests
import base64
import streamlit as st
import streamlit.components.v1 as components

# spotify credentials from secrets.toml
SPOTIFY_CLIENT_ID = st.secrets["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = st.secrets["SPOTIFY_CLIENT_SECRET"] 

# gets tokens to allow spotify API usage
def get_spotify_token():
    auth_string = SPOTIFY_CLIENT_ID + ":" + SPOTIFY_CLIENT_SECRET
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post(url, headers=headers, data=data)
    return response.json()["access_token"]

# Searches for a track on spotify and returns the spotify link and cover image

def search_spotify_track(song_name, artist_name):
    token = get_spotify_token()

    url = "https://api.spotify.com/v1/search"

    headers = {
        "Authorization": "Bearer " + token
    }

    params = {
        "q": f"{song_name} {artist_name}",
        "type": "track",
        "market": "US",
        "limit": 1
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if "tracks" in data and len(data["tracks"]["items"]) > 0:
        track = data["tracks"]["items"][0]

        return {
            "link": track["external_urls"]["spotify"],
            "cover": track["album"]["images"][0]["url"]
        }

    return None

# embedded links for spotify tracks

def show_spotify_embed(track_url):
    embed_url = track_url.replace(
        "https://open.spotify.com/track/",
        "https://open.spotify.com/embed/track/"
    )

    components.iframe(embed_url, height=152)

 # generates similar songs based on mood and audio features

def get_similar_songs(predicted_mood, user_features,  limit=10, genre_keywords=None):
    df = pd.read_csv("spotify_tracks.csv")
    df = df[df["track_name"].str.contains(r"^[A-Za-z0-9\s\.\,\!\?\-\'\&\(\):]+$", regex=True, na=False)]
    df = df[df["artists"].str.contains(r"^[A-Za-z0-9\s\.\,\!\?\-\'\&\(\):]+$", regex=True, na=False)]
    df = df[df["popularity"] >= 80]

    if "mood" not in df.columns:
        df["mood"] = predicted_mood

    mood_songs = df[df["mood"] == predicted_mood].copy()

    if genre_keywords:
        genre_pattern = "|".join(genre_keywords)

        mood_songs = mood_songs[
            mood_songs["track_genre"].str.lower().str.contains(
                genre_pattern,
                na=False
        )
    ]
        

    if len(mood_songs) == 0:
        mood_songs = df.copy()

    feature_columns = [
        "danceability",
        "energy",
        "loudness",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo"
    ]

    # calculates difference between user features and each song

    for feature in feature_columns:
        mood_songs[feature + "_diff"] = abs(
            mood_songs[feature] - user_features[feature]
        )

    mood_songs["similarity_score"] = (
        mood_songs["danceability_diff"] +
        mood_songs["energy_diff"] +
        mood_songs["acousticness_diff"] +
        mood_songs["valence_diff"] +
        mood_songs["tempo_diff"] / 200
    )

    recommendations = mood_songs.sort_values(
    by=["similarity_score", "popularity"],
    ascending=[True, False]
)

    recommendations = recommendations.drop_duplicates(
    subset=["track_name", "artists"]
)

#  # randomly selects songs from recommendations

    if len(recommendations) > limit:
        recommendations = recommendations.sample(limit)
    else:
        recommendations = recommendations.sample(len(recommendations))

    return recommendations
    
