import pandas as pd
import os
from datetime import datetime


def save_playlist(predicted_mood, songs):

    file_name = "saved_playlists.csv"

    saved_rows = []

    for index, row in songs.iterrows():

        saved_rows.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "mood": predicted_mood,
            "song": row["track_name"],
            "artist": row["artists"]
        })

    new_data = pd.DataFrame(saved_rows)

    if os.path.exists(file_name):

        old_data = pd.read_csv(file_name)

        full_data = pd.concat(
            [old_data, new_data],
            ignore_index=True
        )

    else:
        full_data = new_data

    full_data.to_csv(file_name, index=False)


def load_playlist_history():

    file_name = "saved_playlists.csv"

    if os.path.exists(file_name):
        return pd.read_csv(file_name)

    return pd.DataFrame()