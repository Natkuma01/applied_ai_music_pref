"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    # user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    # uncomment below line for testing
    # user_prefs = {"genre": "lofi", "mood": "chill", "energy": 0.35, "valence": 0.5, "danceability": 0.4}

    # testing for phase 4
    test_profiles = [
        {"genre": "pop", "mood": "happy", "energy": 0.8, "valence": 0.8, "danceability": 0.8}, # The "Optimist"
        {"genre": "metal", "mood": "aggressive", "energy": 0.95, "valence": 0.3, "danceability": 0.5}, # The "Intense"
        {"genre": "lofi", "mood": "chill", "energy": 0.2, "valence": 0.5, "danceability": 0.2} # The "Study Session"
    ]

    for profile in test_profiles:
        print(f"\n ---- Testing Profile: {profile['genre']} / {profile['mood']} ---")

    recommendations = recommend_songs(profile, songs, k=5)

    print("\n🎧 Top Recommendations For You 🎧\n")
    for i, rec in enumerate(recommendations, 1):
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"  {i}. 🎶 {song['title']} — ⭐ Score: {score:.2f}")
        print(f"     💡 Because: {explanation}")
        print("-" * 30)



if __name__ == "__main__":
    main()
