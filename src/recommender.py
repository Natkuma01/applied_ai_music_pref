from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import pandas as pd
import numpy as np
import logging
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import csv

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

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
        bonus += 0.2 # 20% boost for genre

    final_score = similarity + bonus
    return final_score

# CHANGE:
#   old way - recommend songs base on if the socre is higher, then the system recommend
#   now - add Guardrails - for example if all 5 recommendations are the same artist or
#                          if the Similarity Score is too low, the system will log a warning:
#                          "Low confidence recommendation: Dataset lacks low-energy songs"
def recommend_songs(user_prefs: Dict, songs_list: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    df = pd.DataFrame(songs_list)
    results = []
    
    for _, row in df.iterrows():
        # Convert row to a small dataframe for our scorer
        song_df = pd.DataFrame([row])
        score = score_song(user_prefs, song_df)
        results.append((row.to_dict(), score))
        
    # Sort by score
    results.sort(key=lambda x: x[1], reverse=True)
    top_k = results[:k]
    
    # --- GUARDRAIL CHECK ---
    # If the top recommendation score is very low, log a warning
    if top_k[0][1] < 0.5:
        logging.warning(f"Low confidence for user pref: {user_prefs['genre']}. No good matches found.")
        
    return top_k
