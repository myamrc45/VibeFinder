import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load the dataset
df = pd.read_csv("spotify_tracks.csv")

# Create mood labels based on song features
def create_mood(row):

    if row["energy"] > 0.75 and row["danceability"] > 0.65:
        return "Energetic"

    elif row["energy"] > 0.6 and row["danceability"] > 0.6:
        return "Happy"

    elif row["energy"] < 0.4 and row["danceability"] < 0.5:
        return "Sad"

    elif row["energy"] < 0.5 and row["acousticness"] > 0.4:
        return "Chill"

    elif row["energy"] > 0.3 and row["energy"] < 0.7:
        return "Romantic"

    else:
        return "Chill"


df["mood"] = df.apply(create_mood, axis=1)

# Features the model will learn from
features = [
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

X = df[features]
y = df["mood"]

# Split data into training and testing groups
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create and train the model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)


predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("Model Accuracy:", accuracy)


# Save the trained model
joblib.dump(model, "mood_model.pkl")

print("Model trained and saved as mood_model.pkl")