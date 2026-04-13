"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import re
from tabulate import tabulate
from recommender import load_songs, recommend_songs, STRATEGY_WEIGHTS


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


def _score_bar(score: float, max_score: float = 14.0, width: int = 10) -> str:
    """Return a block-character progress bar for the given score."""
    filled = max(0, min(width, round((score / max_score) * width)))
    return "█" * filled + "░" * (width - filled) + f"  {score:.1f}"


def _top_reasons(explanation: str, n: int = 3) -> list:
    """Return the top n reasons sorted by point contribution, skipping zero-point entries."""
    parts = explanation.split(" | ")
    scored_parts = []
    for part in parts:
        m = re.search(r'\(\+(\d+\.?\d*)\)', part)
        pts = float(m.group(1)) if m else 0.0
        if pts > 0:
            scored_parts.append((pts, part))
    scored_parts.sort(reverse=True)
    return [p for _, p in scored_parts[:n]]


def print_recommendations(profile_name: str, user_prefs: dict, recommendations: list,
                          strategy: str = "balanced", adversarial: bool = False) -> None:
    """Print a formatted recommendations block for one profile."""
    if adversarial:
        tag = "ADVERSARIAL TEST"
    else:
        tag = f"STRATEGY: {strategy.upper().replace('_', '-')}"
    print()
    print("=" * 62)
    print(f"  {profile_name.upper()}")
    print(f"  [{tag}]")
    print(f"  Genre: {user_prefs['genre']}  |  Mood: {user_prefs['mood']}  |  Energy: {user_prefs['energy']}")
    print("=" * 62)

    table_rows = []
    for rank, (song, score, _) in enumerate(recommendations, start=1):
        table_rows.append([
            f"#{rank}",
            song["title"],
            song["artist"],
            _score_bar(score),
            song["genre"],
            song["mood"],
        ])
    print(tabulate(table_rows, headers=["", "Title", "Artist", "Score", "Genre", "Mood"],
                   tablefmt="rounded_outline"))

    for rank, (song, _, explanation) in enumerate(recommendations, start=1):
        top = _top_reasons(explanation)
        print(f"\n  #{rank} {song['title']} — top reasons:")
        for reason in top:
            print(f"       • {reason}")

    print()


def print_diversity_comparison(profile_name: str, user_prefs: dict,
                               songs: list, k: int = 5) -> None:
    """Print side-by-side: top-k without diversity vs with diversity penalties."""
    without = recommend_songs(user_prefs, songs, k=k, strategy="balanced")
    with_div = recommend_songs(user_prefs, songs, k=k, strategy="balanced",
                               artist_penalty=2.0, genre_penalty=1.0)

    print()
    print("=" * 62)
    print(f"  DIVERSITY COMPARISON — {profile_name.upper()}")
    print(f"  artist_penalty=2.0  |  genre_penalty=1.0")
    print("=" * 62)

    rows = []
    for i, ((s1, sc1, _), (s2, sc2, _)) in enumerate(zip(without, with_div), 1):
        changed = "" if s1["title"] == s2["title"] else "←"
        rows.append([
            f"#{i}",
            f"{s1['title']} ({sc1:.1f})",
            f"{s2['title']} ({sc2:.1f})",
            changed,
        ])
    print(tabulate(rows, headers=["", "No Diversity", "With Diversity", ""],
                   tablefmt="rounded_outline"))
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    # --- Standard profiles across all strategies ---
    for profile_name, user_prefs in PROFILES.items():
        for strategy in ("balanced", "genre_first", "mood_first", "energy_focused"):
            recommendations = recommend_songs(user_prefs, songs, k=3, strategy=strategy)
            print_recommendations(profile_name, user_prefs, recommendations, strategy=strategy)

    # --- Diversity comparison (Chill Lofi best demonstrates artist clustering) ---
    print_diversity_comparison("Chill Lofi",         PROFILES["Chill Lofi"],        songs, k=5)
    print_diversity_comparison("High-Energy Pop",    PROFILES["High-Energy Pop"],   songs, k=5)
    print_diversity_comparison("Deep Intense Rock",  PROFILES["Deep Intense Rock"], songs, k=5)

    # --- Adversarial profiles ---
    for profile_name, user_prefs in ADVERSARIAL_PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=3)
        print_recommendations(profile_name, user_prefs, recommendations, adversarial=True)


if __name__ == "__main__":
    main()
