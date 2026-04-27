from src.recommender import load_songs, recommend_songs, prepare_data


def main() -> None:
    raw_songs = load_songs("data/songs.csv") 

    df_songs, music_scaler = prepare_data(raw_songs)

    test_profiles = [
        # HIGH CONFIDENCE CASES (genre matches + good scores)
        {"genre": "pop", "mood": "happy", "energy": 0.8, "valence": 0.8, "danceability": 0.8, "tempo_bpm": 120}, # The "Optimist" - ✅ pop exists
        {"genre": "lofi", "mood": "chill", "energy": 0.4, "valence": 0.6, "danceability": 0.6, "acousticness": 0.8, "tempo_bpm": 75}, # The "Chill Seeker" - ✅ lofi exists
        
        # EDGE CASES (trigger guardrail warning - extremely niche/contradictory preferences)
        {"genre": "punk", "mood": "rebellious", "energy": 0.02, "valence": 0.01, "danceability": 0.01, "acousticness": 0.01, "tempo_bpm": 30}, # The "Silent Punk" - extreme opposite to all songs
    ]

    for profile in test_profiles:
        print(f"\n ---- Testing Profile: {profile['genre']} / {profile['mood']} ---")

        recommendations = recommend_songs(profile, df_songs, music_scaler, k=5)

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
