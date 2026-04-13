from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

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

    The four original fields are required (no defaults).
    New numeric targets are optional with neutral mid-range defaults so
    existing tests keep passing without modification.
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    # Extended taste targets added to support the full scoring formula
    target_valence: float = 0.5
    target_danceability: float = 0.5
    target_tempo_bpm: float = 100.0
    target_speechiness: float = 0.05
    target_instrumentalness: float = 0.30


# ---------------------------------------------------------------------------
# Example taste profiles — each represents a distinct listening archetype.
#
# How to read these:
#   - target_energy / target_valence etc. map to the 0.0–1.0 feature scale
#   - target_tempo_bpm is in raw BPM (normalized inside the scorer)
#   - likes_acoustic=True  → derives target_acousticness ≈ 0.78
#     likes_acoustic=False → derives target_acousticness ≈ 0.18
#
# CHILL_STUDY vs INTENSE_WORKOUT are deliberately maximally different so
# the recommender can be verified to score Library Rain >> Gym Hero for one
# profile, and the reverse for the other.
# ---------------------------------------------------------------------------

PROFILE_CHILL_STUDY = UserProfile(
    favorite_genre="lofi",
    favorite_mood="focused",
    target_energy=0.38,
    likes_acoustic=True,
    target_valence=0.58,
    target_danceability=0.55,
    target_tempo_bpm=78.0,
    target_speechiness=0.03,
    target_instrumentalness=0.75,
)

PROFILE_INTENSE_WORKOUT = UserProfile(
    favorite_genre="rock",
    favorite_mood="intense",
    target_energy=0.93,
    likes_acoustic=False,
    target_valence=0.55,
    target_danceability=0.85,
    target_tempo_bpm=145.0,
    target_speechiness=0.07,
    target_instrumentalness=0.05,
)

PROFILE_SAD_EVENING = UserProfile(
    favorite_genre="blues",
    favorite_mood="melancholic",
    target_energy=0.32,
    likes_acoustic=True,
    target_valence=0.22,
    target_danceability=0.40,
    target_tempo_bpm=72.0,
    target_speechiness=0.05,
    target_instrumentalness=0.40,
)

PROFILE_DANCE_PARTY = UserProfile(
    favorite_genre="edm",
    favorite_mood="euphoric",
    target_energy=0.95,
    likes_acoustic=False,
    target_valence=0.90,
    target_danceability=0.93,
    target_tempo_bpm=138.0,
    target_speechiness=0.03,
    target_instrumentalness=0.80,
)

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    # TODO: Implement CSV loading logic
    print(f"Loading songs from {csv_path}...")
    return []

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # TODO: Implement scoring and ranking logic
    # Expected return format: (song_dict, score, explanation)
    return []
