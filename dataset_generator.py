import pandas as pd
import random
from datetime import datetime, timedelta
import os

# Create output folder
os.makedirs("data", exist_ok=True)

# Song metadata generation
song_ids = [f"song_{i}" for i in range(1, 101)]
titles = [f"Song Title {i}" for i in range(1, 101)]
artists = [f"Artist {i%10}" for i in range(1, 101)]
genres = ["Pop", "Rock", "Jazz", "Electronic", "HipHop", "Sad", "Happy"]
moods = ["Happy", "Sad", "Energetic", "Chill"]

songs_metadata = {
    "song_id": song_ids,
    "title": titles,
    "artist": artists,
    "genre": [random.choice(genres) for _ in song_ids],
    "mood": [random.choice(moods) for _ in song_ids]
}

df_songs = pd.DataFrame(songs_metadata)
df_songs.to_csv("data/songs_metadata.csv", index=False)
print("✅ songs_metadata.csv generated.")

# Listening logs generation
user_ids = [f"user_{i}" for i in range(1, 21)]
logs = []

for user in user_ids:
    for _ in range(random.randint(80, 150)):
        # Increase genre bias for user_1 and user_2
        if user in ["user_1", "user_2"]:
            sad_songs = df_songs[df_songs["genre"] == "Sad"]["song_id"].tolist()
            song_id = random.choice(sad_songs) if sad_songs and random.random() < 0.8 else random.choice(song_ids)
        else:
            song_id = random.choice(song_ids)

        # Random timestamp in the last 14 days
        random_days = random.randint(0, 13)
        random_time = datetime.now() - timedelta(days=random_days, hours=random.randint(0, 23), minutes=random.randint(0, 59))
        duration = random.randint(30, 300)

        logs.append({
            "user_id": user,
            "song_id": song_id,
            "timestamp": random_time.strftime("%Y-%m-%d %H:%M:%S"),
            "duration_sec": duration
        })

df_logs = pd.DataFrame(logs)
df_logs.to_csv("data/listening_logs.csv", index=False)
print("✅ listening_logs.csv generated.")
