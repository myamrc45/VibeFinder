import pandas as pd
import requests
import base64
import streamlit as st
import streamlit.components.v1 as components


SPOTIFY_CLIENT_ID = st.secrets["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = st.secrets["SPOTIFY_CLIENT_SECRET"]


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

    if response.status_code != 200:
        return None

    try:
        token_data = response.json()
        return token_data["access_token"]
    except Exception:
        return None


def search_spotify_track(song_name, artist_name):
    token = get_spotify_token()

    if token is None:
        return None

    url = "https://api.spotify.com/v1/search"

    headers = {
        "Authorization": "Bearer " + token
    }

    query = f"{song_name} {artist_name}"
    query = query.replace('"', "")

    params = {
        "q": query,
        "type": "track",
        "market": "US",
        "limit": 1
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        return None

    try:
        data = response.json()
    except Exception:
        return None

    if "tracks" not in data:
        return None

    if "items" not in data["tracks"]:
        return None

    if len(data["tracks"]["items"]) == 0:
        return None

    track = data["tracks"]["items"][0]

    cover = ""

    if track["album"]["images"]:
        cover = track["album"]["images"][0]["url"]

    return {
        "link": track["external_urls"]["spotify"],
        "cover": cover,
        "name": track["name"],
        "artist": track["artists"][0]["name"]
    }


def show_spotify_embed(track_url):
    if track_url is None:
        return

    embed_url = track_url.replace(
        "https://open.spotify.com/track/",
        "https://open.spotify.com/embed/track/"
    )

    components.iframe(
        embed_url,
        height=152,
        scrolling=False
    )


def get_similar_songs(predicted_mood, user_features, limit=10, genre_keywords=None):
    df = pd.read_csv("spotify_tracks.csv")

    df = df[df["track_name"].str.contains(r"^[A-Za-z0-9\s\.\,\!\?\-\'\&\(\)]+$", regex=True, na=False)]
    df = df[df["artists"].str.contains(r"^[A-Za-z0-9\s\.\,\!\?\-\'\&\(\)]+$", regex=True, na=False)]

    if "popularity" in df.columns:
        df = df[df["popularity"] >= 20]

    if "mood" not in df.columns:
        df["mood"] = predicted_mood

    mood_songs = df[df["mood"] == predicted_mood].copy()

    if genre_keywords and "track_genre" in mood_songs.columns:
        genre_pattern = "|".join(genre_keywords)

        mood_songs = mood_songs[
            mood_songs["track_genre"].astype(str).str.lower().str.contains(
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

    for feature in feature_columns:
        if feature in mood_songs.columns and feature in user_features:
            mood_songs[feature + "_diff"] = abs(
                mood_songs[feature] - user_features[feature]
            )

    mood_songs["similarity_score"] = 0

    for feature in feature_columns:
        diff_col = feature + "_diff"

        if diff_col in mood_songs.columns:
            if feature == "tempo":
                mood_songs["similarity_score"] += mood_songs[diff_col] / 200
            elif feature == "loudness":
                mood_songs["similarity_score"] += mood_songs[diff_col] / 60
            else:
                mood_songs["similarity_score"] += mood_songs[diff_col]

    recommendations = mood_songs.sort_values(
        by=["similarity_score", "popularity"],
        ascending=[True, False]
    )

    recommendations = recommendations.drop_duplicates(
        subset=["track_name", "artists"]
    )

    top_matches = recommendations.head(50)

    if len(top_matches) > limit:
        recommendations = top_matches.sample(limit)
    else:
        recommendations = top_matches

    return recommendations