"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print()
    print("=" * 52)
    print("  MUSIC RECOMMENDER — TOP PICKS FOR YOUR PROFILE")
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


if __name__ == "__main__":
    main()
