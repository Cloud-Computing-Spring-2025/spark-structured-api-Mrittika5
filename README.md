
# Music Streaming Analytics - Assignment README

## 📄 Overview
This assignment simulates a mini music streaming analytics platform using synthetic datasets. It includes a dataset generator and a Python analytics script that mimics typical streaming data analysis tasks. The goal is to analyze user behavior and song characteristics using PySpark or a similar data processing approach.

## 📅 Datasets

### 1. `songs_metadata.csv`
- **song_id**: Unique identifier for each song.
- **title**: Title of the song.
- **artist**: Artist name.
- **genre**: Music genre (e.g., Pop, Rock, Jazz).
- **mood**: Mood category (e.g., Happy, Sad, Energetic, Chill).

### 2. `listening_logs.csv`
- **user_id**: Unique identifier for each user.
- **song_id**: ID of the song played.
- **timestamp**: Date and time of song play.
- **duration_sec**: Duration (in seconds) of listening activity.

## 📊 Output Description and Task Breakdown
All output files are saved in the `output/` directory, categorized into subfolders for each task.

### Task 1: User's Favorite Genre
**File**: `output/user_favorite_genres/user_favorite_genres.csv`
- Identifies the most frequently played genre by each user.
- Grouped by `user_id` and `genre`, counted, then sorted by count to get the favorite genre.

### Task 2: Average Listen Time per Song
**File**: `output/avg_listen_time_per_song/avg_listen_time_per_song.csv`
- Calculates the average `duration_sec` each song was played.
- Grouped by `song_id` and averaged across play history.

### Task 3: Top 10 Most Played Songs This Week
**File**: `output/top_songs_this_week/top_songs_this_week.csv`
- Filters logs for the current week based on `timestamp`.
- Aggregates play counts per song and returns the top 10.

### Task 4: Happy Song Recommendations for Sad Listeners
**File**: `output/happy_recommendations/happy_recommendations.csv`
- Identifies users who predominantly listen to "Sad" genre songs.
- Recommends up to 3 "Happy" mood songs they haven't played before.

### Task 5: Genre Loyalty Score
**File**: `output/genre_loyalty_scores/genre_loyalty_scores.csv`
- For each user, calculates: 
  `loyalty_score = plays in most played genre / total plays`
- Filters users with a loyalty score above 0.8.

### Task 6: Night Owl Users
**File**: `output/night_owl_users/night_owl_users.csv`
- Filters logs between 12:00 AM to 5:00 AM.
- Groups by `user_id` to count night-time plays.

### Task 7: Enriched Logs
**File**: `output/enriched_logs/enriched_logs.csv`
- Merges `listening_logs.csv` with `songs_metadata.csv` on `song_id`.
- Produces enriched view with timestamp, user, song, genre, mood, and duration.

## 🔢 Running the Code

### Step 1: Generate Datasets
```bash
python generate_datasets.py
```
This will create `songs_metadata.csv` and `listening_logs.csv` under the `data/` folder.

### Step 2: Run All Analysis Tasks
```bash
python run_tasks.py
```
This script will generate results for all 7 tasks under the `output/` directory.

### Optionally (for Spark users):
```bash
pyspark
```
```python
spark.read.csv("data/listening_logs.csv", header=True, inferSchema=True)
```

## ❌ Errors Encountered and Fixes

### Issue: Empty `genre_loyalty_scores.csv`
**Cause**: Users had diverse genre listening patterns, preventing any single genre from exceeding the 0.8 threshold.
**Fix**: Updated the dataset generator to bias specific users toward one genre to ensure high loyalty scores.

### Issue: Missing `enriched_logs.csv`
**Cause**: File saving line was missing in `run_tasks.py`.
**Fix**: Added `.to_csv("output/enriched_logs/enriched_logs.csv", index=False)` to save the merged dataset.

## 📃 Screenshots (Add if applicable)
If run via Jupyter, screenshots of CSV previews (e.g., using `df.head()`) can be included here.

---

This README outlines the complete pipeline of dataset generation, task execution, and results output for a mini music streaming analytics engine. All logic is written in Python using Pandas but designed in a way that it can be ported to PySpark with minor changes.
