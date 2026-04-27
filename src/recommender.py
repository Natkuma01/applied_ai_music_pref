from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import pandas as pd
import numpy as np
import logging
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import csv


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
        }
        scored = sorted(self.songs, key=lambda s: score_song(user_prefs, vars(s))[0], reverse=True)
        return scored[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
        }
        _, reasons = score_song(user_prefs, vars(song))
        return ", ".join(reasons) if reasons else "general match"


# ADD: Data Prep - use MinMaxScaler - use prepare_data() to scaling the data
#                  Tempo was (60-170) and Energy was (0-1). --> unfair scaling
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')             # <--- Logging
def prepare_data(songs_list):

    df = pd.DataFrame(songs_list)
    
    # Define which columns are numerical
    features = ['energy', 'valence', 'danceability', 'acousticness', 'tempo_bpm']
    
    # Initialize the Scaler
    scaler = MinMaxScaler()
    
    # This 'scales' the numbers to be between 0 and 1
    # so now let's say Tempo is 120 in the old scale system, now become 0.5 (with the scaling range that is from 0 to 1)
    df[features] = scaler.fit_transform(df[features])
    
    return df, scaler

# This is a safety check: it reutrn True if the match is decent
# the threshold is saying if the "similarity score" is less than 40%, then warning message will be sent
def check_guardrail(score, threshold=0.4):
    if score < threshold:
        logging.warning(f"Guardrail Triggered: Low similarity score ({score:.2f})")
        return False
    return True

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    int(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    print(f"Loaded songs: {len(songs)}")
    return songs


# CHANGE: not use score/adding points system, calculate the Cosine Cimilarity btw user's Ideal Vector
#         and the song's Feature Vector
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')        # <-- Logging
def score_song(user_prefs: dict, song_df: pd.DataFrame):
    score = 0.0
    reasons = []

    # 1. define the features we want the AI to look at 
    features = ['energy', 'valence', 'danceability', 'acousticness']

    # 2. prepare the data - turn the user's dream features into a tiny list(vector)
    user_vector = np.array([[user_prefs[f] for f in features]])

    # 3. take the song's features
    song_vector = song_df[features].values.reshape(1, -1)

    # 4. Calculate Cosine Similarity
    #    Result is btw 0(no match) and 1(perfect match)
    similarity = cosine_similarity(user_vector, song_vector)[0][0]

    # 5. if the genre/ modd match ==> boost
    bonus = 0
    if song_df['genre'].iloc[0].lower() == user_prefs['genre'].lower():
        bonus += 0.1 # 10% boost for genre

    final_score = similarity + bonus
    return final_score

# CHANGE:
#   old way - recommend songs base on if the socre is higher, then the system recommend
#   now - add Guardrails - for example if all 5 recommendations are the same artist or
#                          if the Similarity Score is too low, the system will log a warning:
#                          "Low confidence recommendation: Dataset lacks low-energy songs"
def recommend_songs(user_prefs: Dict, df: pd.DataFrame, scaler: MinMaxScaler, k: int = 5):
    
    # prepare & scale the user's preferd song
    # create a small dataframe of user's numerical goals
    user_features = pd.DataFrame([{
        'energy': user_prefs.get('energy', 0.5),              # <--- set a default value if user forget to fill out one part of their profile
        'valence': user_prefs.get('valence',0.5),
        'danceability': user_prefs.get('danceability', 0.5),
        'acousticness': user_prefs.get('acousticness', 0.5),
        'tempo_bpm': user_prefs.get('tempo_bpm', 120)    
    }])  

    # use the scaler to turn the User BPM(like the Tempo was 120) into the 0 to 1 scale
    user_scaled = scaler.transform(user_features)
    
    results = []
    features = ['energy', 'valence', 'danceability', 'acousticness', 'tempo_bpm']

    for _, row in df.iterrows():

        # get this specific song's numerical vector
        song_vector = row[features].values.reshape(1, -1)

        similarity = cosine_similarity(user_scaled, song_vector)[0][0]
        score = similarity

        reason = "Good vibe match"              # <--- a simple explanation for user

        if row['genre'].lower() == user_prefs['genre'].lower():
            score += 0.1
            reason = f"Excellent match for your {row['genre']} preference"
        results.append((row.to_dict(), score, reason))

    # sort and apply the guardrail
    results.sort(key=lambda x: x[1], reverse=True)
    top_k = results[:k]
    
    best_song_data = top_k[0][0]
    best_score = top_k[0][1]

    genre_matches = best_song_data['genre'].lower() == user_prefs['genre'].lower()

    if not genre_matches and best_score < 0.8:
        print(f"\n⚠️  WARNING: This is not the best recommendation, but it's the closest match I found.")
        print(f"💡 Suggestion: Your dataset lacks enough '{user_prefs['genre']}' songs or matches for your '{user_prefs['mood']}' vibe.")
    else:
        logging.info(f"High confidence match found with score: {best_score:.2f}")
        
    return top_k