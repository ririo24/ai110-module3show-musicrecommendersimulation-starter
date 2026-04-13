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


# ---------------------------------------------------------------------------
# Adversarial profiles — designed to expose edge cases and scoring biases.
# Each has a comment explaining what contradiction or boundary it tests.
# ---------------------------------------------------------------------------
ADVERSARIAL_PROFILES = {
    # Tests: numeric features (high energy) vs categorical mood (sad).
    # Mood "sad" never appears in rock/metal songs — mood bonus will always be 0.
    # Does high energy pull Storm Runner to #1 even though the user wants sad music?
    "Sad Banger": {
        "genre":                   "rock",
        "mood":                    "sad",
        "energy":                  0.92,
        "likes_acoustic":          False,
        "target_valence":          0.15,
        "target_danceability":     0.72,
        "target_tempo_bpm":        148.0,
        "target_speechiness":      0.07,
        "target_instrumentalness": 0.05,
    },
    # Tests: both genre and mood are not in the dataset ("country", "content").
    # Categorical bonuses are permanently 0 for every song.
    # Exposes the mediocrity bias — scores cluster tightly with no clear winner.
    "The Fence-Sitter": {
        "genre":                   "country",
        "mood":                    "content",
        "energy":                  0.50,
        "likes_acoustic":          False,
        "target_valence":          0.50,
        "target_danceability":     0.50,
        "target_tempo_bpm":        110.0,
        "target_speechiness":      0.05,
        "target_instrumentalness": 0.10,
    },
    # Tests: likes_acoustic=True forces target_acousticness=0.78,
    # but genre="edm" and mood="euphoric" pull toward low-acousticness electronic songs.
    # A direct contradiction — can no song satisfy both constraints?
    "Acoustic Raver": {
        "genre":                   "edm",
        "mood":                    "euphoric",
        "energy":                  0.95,
        "likes_acoustic":          True,
        "target_valence":          0.90,
        "target_danceability":     0.93,
        "target_tempo_bpm":        138.0,
        "target_speechiness":      0.03,
        "target_instrumentalness": 0.80,
    },
    # Tests: extreme target_speechiness=0.90 — only Concrete Jungle (0.72) is close.
    # But speechiness weight is only 0.5 pts max. Does one feature dominate the ranking,
    # or does it get washed out by the 7 other features?
    "Speechiness Hunter": {
        "genre":                   "hip-hop",
        "mood":                    "energetic",
        "energy":                  0.85,
        "likes_acoustic":          False,
        "target_valence":          0.62,
        "target_danceability":     0.84,
        "target_tempo_bpm":        95.0,
        "target_speechiness":      0.90,
        "target_instrumentalness": 0.02,
    },
}


def print_recommendations(profile_name: str, user_prefs: dict, recommendations: list,
                          strategy: str = "balanced", adversarial: bool = False) -> None:
    """Print a formatted recommendations block for one profile."""
    if adversarial:
        tag = "ADVERSARIAL TEST"
    else:
        tag = f"STRATEGY: {strategy.upper().replace('_', '-')}"
    print()
    print("=" * 52)
    print(f"  {profile_name.upper()}")
    print(f"  [{tag}]")
    print("=" * 52)
    print(f"  Genre: {user_prefs['genre']}  |  Mood: {user_prefs['mood']}  |  Energy: {user_prefs['energy']}")
    print("=" * 52)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print()
        print(f"  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       Score: {score:.2f}")
        print(f"       Genre: {song['genre']}  |  Mood: {song['mood']}")
        print()
        for reason in explanation.split(" | "):
            print(f"         • {reason}")
        print()
        print("  " + "-" * 50)

    print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    # --- Standard profiles, each run under all four strategies ---
    # Swap the strategy name to see how rankings shift.
    for profile_name, user_prefs in PROFILES.items():
        for strategy in ("balanced", "genre_first", "mood_first", "energy_focused"):
            recommendations = recommend_songs(user_prefs, songs, k=3, strategy=strategy)
            print_recommendations(profile_name, user_prefs, recommendations, strategy=strategy)

    # --- Adversarial profiles (balanced strategy only) ---
    for profile_name, user_prefs in ADVERSARIAL_PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=3)
        print_recommendations(profile_name, user_prefs, recommendations, adversarial=True)


if __name__ == "__main__":
    main()
