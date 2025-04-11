
import pandas as pd
import os
from datetime import datetime

# Create output directory structure
output_dirs = [
    "output/user_favorite_genres",
    "output/avg_listen_time_per_song",
    "output/top_songs_this_week",
    "output/happy_recommendations",
    "output/genre_loyalty_scores",
    "output/night_owl_users",
    "output/enriched_logs"
]

for dir in output_dirs:
    os.makedirs(dir, exist_ok=True)

# Load datasets
df_logs = pd.read_csv("data/listening_logs.csv")
df_songs = pd.read_csv("data/songs_metadata.csv")

# Enriched logs (merge logs with songs metadata)
df_logs['timestamp'] = pd.to_datetime(df_logs['timestamp'])
enriched_logs = df_logs.merge(df_songs, on="song_id")

# Save enriched logs
enriched_logs.to_csv("output/enriched_logs/enriched_logs.csv", index=False)
print("Enriched logs saved.")

# Task 1: Find each user’s favorite genre
user_genre_counts = enriched_logs.groupby(['user_id', 'genre']).size().reset_index(name='count')
user_favorite_genre = user_genre_counts.sort_values(['user_id', 'count'], ascending=[True, False]).drop_duplicates('user_id')
user_favorite_genre.to_csv("output/user_favorite_genres/user_favorite_genres.csv", index=False)

# Task 2: Calculate the average listen time per song
avg_listen_time = enriched_logs.groupby(['song_id', 'title'])['duration_sec'].mean().reset_index()
avg_listen_time.to_csv("output/avg_listen_time_per_song/avg_listen_time_per_song.csv", index=False)

# Task 3: List the top 10 most played songs this week
week_num = datetime.now().isocalendar()[1]
enriched_logs['week'] = enriched_logs['timestamp'].dt.isocalendar().week
top_songs_this_week = enriched_logs[enriched_logs['week'] == week_num]
top_songs = top_songs_this_week.groupby(['song_id', 'title']).size().reset_index(name='play_count')
top_songs = top_songs.sort_values('play_count', ascending=False).head(10)
top_songs.to_csv("output/top_songs_this_week/top_songs_this_week.csv", index=False)

# Task 4: Recommend "Happy" songs to users who mostly listen to "Sad" songs
user_genre_counts = enriched_logs.groupby(['user_id', 'genre']).size().reset_index(name='count')
sad_user_total_counts = enriched_logs.groupby('user_id').size().reset_index(name='total')
sad_user_sad_counts = user_genre_counts[user_genre_counts['genre'] == 'Sad']
sad_user_ratio = pd.merge(sad_user_sad_counts, sad_user_total_counts, on='user_id')
sad_user_ratio['sad_ratio'] = sad_user_ratio['count'] / sad_user_ratio['total']
sad_users = sad_user_ratio[sad_user_ratio['sad_ratio'] > 0.5]['user_id']

happy_songs = df_songs[df_songs['mood'] == 'Happy']
played_songs = enriched_logs[['user_id', 'song_id']].drop_duplicates()
recommendations = []

for user in sad_users:
    played_songs_by_user = set(played_songs[played_songs['user_id'] == user]['song_id'])
    happy_songs_to_recommend = happy_songs[~happy_songs['song_id'].isin(played_songs_by_user)]
    recs = happy_songs_to_recommend.head(3).copy()
    recs['user_id'] = user
    recommendations.append(recs)

recommendations_df = pd.concat(recommendations) if recommendations else pd.DataFrame()
recommendations_df.to_csv("output/happy_recommendations/happy_recommendations.csv", index=False)

# Task 5: Compute the genre loyalty score for each user
user_total_plays = enriched_logs.groupby('user_id').size().reset_index(name='total_plays')
user_genre_plays = enriched_logs.groupby(['user_id', 'genre']).size().reset_index(name='genre_plays')
max_genre_by_user = user_genre_plays.sort_values(['user_id', 'genre_plays'], ascending=[True, False])
most_played_genres = max_genre_by_user.drop_duplicates('user_id')
user_loyalty = pd.merge(most_played_genres, user_total_plays, on='user_id')
user_loyalty['loyalty_score'] = user_loyalty['genre_plays'] / user_loyalty['total_plays']

# Debug: Show top loyalty scores
print("\n Top loyalty scores:")
print(user_loyalty[['user_id', 'genre', 'loyalty_score']].sort_values('loyalty_score', ascending=False).head(10))

loyal_users = user_loyalty[user_loyalty['loyalty_score'] > 0.8]
if not loyal_users.empty:
    loyal_users.to_csv("output/genre_loyalty_scores/genre_loyalty_scores.csv", index=False)
    print("✅ Genre loyalty scores saved.")
else:
    print("⚠️ No users with loyalty score > 0.8. Consider increasing genre concentration in data.")

# Task 6: Identify night owl users (12 AM - 5 AM)
enriched_logs['hour'] = enriched_logs['timestamp'].dt.hour
night_owls = enriched_logs[(enriched_logs['hour'] >= 0) & (enriched_logs['hour'] < 5)]
night_owl_users = night_owls.groupby('user_id').size().reset_index(name='night_plays')
night_owl_users.to_csv("output/night_owl_users/night_owl_users.csv", index=False)
