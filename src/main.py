"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


PROFILES = {
    "High-Energy Pop": {
        "genre":                   "pop",
        "mood":                    "happy",
        "energy":                  0.88,
        "likes_acoustic":          False,
        "target_valence":          0.85,
        "target_danceability":     0.86,
        "target_tempo_bpm":        126.0,
        "target_speechiness":      0.08,
        "target_instrumentalness": 0.02,
    },
    "Chill Lofi": {
        "genre":                   "lofi",
        "mood":                    "focused",
        "energy":                  0.38,
        "likes_acoustic":          True,
        "target_valence":          0.58,
        "target_danceability":     0.55,
        "target_tempo_bpm":        78.0,
        "target_speechiness":      0.03,
        "target_instrumentalness": 0.75,
    },
    "Deep Intense Rock": {
        "genre":                   "rock",
        "mood":                    "intense",
        "energy":                  0.92,
        "likes_acoustic":          False,
        "target_valence":          0.45,
        "target_danceability":     0.68,
        "target_tempo_bpm":        148.0,
        "target_speechiness":      0.07,
        "target_instrumentalness": 0.06,
    },
}


def print_recommendations(profile_name: str, user_prefs: dict, recommendations: list) -> None:
    """Print a formatted recommendations block for one profile."""
    print()
    print("=" * 52)
    print(f"  {profile_name.upper()}")
    print("=" * 52)
    print(f"  Genre: {user_prefs['genre']}  |  Mood: {user_prefs['mood']}  |  Energy: {user_prefs['energy']}")
    print("=" * 52)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print()
        print(f"  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       Score: {score:.2f} / 10.0")
        print(f"       Genre: {song['genre']}  |  Mood: {song['mood']}")
        print()
        for reason in explanation.split(" | "):
            print(f"         • {reason}")
        print()
        print("  " + "-" * 50)

    print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    for profile_name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(profile_name, user_prefs, recommendations)


if __name__ == "__main__":
    main()
