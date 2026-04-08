from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
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

def score_song(user_prefs, song):
    """Scores a song against user preferences by awarding points for matching
    genre, mood, energy, tempo, and other audio features."""
    score = 0.0
    reasons = []

    # 1. Genre Match (+3.0)
    if song['genre'].lower() == user_prefs['genre'].lower():
        score += 3.0
        reasons.append(f"Genre match: {song['genre']} (+3.0)")

    # 2. Mood Match (+2.0)
    if song['mood'].lower() == user_prefs['mood'].lower():
        score += 2.0
        reasons.append(f"Mood match: {song['mood']} (+2.0)")

    # 3. Energy Similarity (up to +1.0)
    energy_diff = abs(song['energy'] - user_prefs['energy'])
    energy_score = 1.0 * (1 - energy_diff)
    score += energy_score
    reasons.append(f"Energy fit (+{energy_score:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    ranked_results = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        ranked_results.append((song, score, reasons))
    ranked_results = sorted(ranked_results, key=lambda x: x[1], reverse=True)
    return ranked_results[:k]
