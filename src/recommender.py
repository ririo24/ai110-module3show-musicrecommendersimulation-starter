from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
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
    speechiness: float = 0.05
    instrumentalness: float = 0.10
    # New attributes
    popularity: int = 50
    release_decade: int = 2010
    liveness: float = 0.10
    explicit: int = 0
    mood_tags: str = ""

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
    # New preference fields
    target_popularity: float = 50.0
    popularity_preference: str = "neutral"   # "mainstream", "underground", or "neutral"
    target_decade: int = 2010
    target_liveness: float = 0.15
    allow_explicit: bool = True
    desired_mood_tags: List[str] = field(default_factory=list)


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
        """Return the top k songs ranked by score for the given user profile."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable string explaining why a song was recommended."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Parse a CSV file of songs and return a list of dicts with typed values."""
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            songs.append({
                "id":               int(row["id"]),
                "title":            row["title"],
                "artist":           row["artist"],
                "genre":            row["genre"],
                "mood":             row["mood"],
                "energy":           float(row["energy"]),
                "tempo_bpm":        float(row["tempo_bpm"]),
                "valence":          float(row["valence"]),
                "danceability":     float(row["danceability"]),
                "acousticness":     float(row["acousticness"]),
                "speechiness":      float(row.get("speechiness", 0.05)),
                "instrumentalness": float(row.get("instrumentalness", 0.10)),
                "popularity":       int(row.get("popularity", 50)),
                "release_decade":   int(row.get("release_decade", 2010)),
                "liveness":         float(row.get("liveness", 0.10)),
                "explicit":         int(row.get("explicit", 0)),
                "mood_tags":        row.get("mood_tags", "").split("|"),
            })
    print(f"  Loaded {len(songs)} songs.")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences and return a list of reasons.

    Score breakdown (max ~13.7):
      Original features  — mood(2.0) genre(1.5) energy(2.0) valence(1.5)
                           acousticness(1.0) danceability(0.8) speechiness(0.5)
                           instrumentalness(0.5) tempo(0.2)          = 10.0
      New features       — mood_tags(1.5) popularity(0.8) decade(0.7)
                           liveness(0.4) explicit(0.3)               =  3.7
    """
    TEMPO_MIN, TEMPO_MAX = 60.0, 180.0
    score = 0.0
    reasons = []

    # --- Categorical: mood (+2.0 exact match, else +0.0) ---
    if user_prefs.get("mood") == song["mood"]:
        score += 2.0
        reasons.append(f"mood match: '{song['mood']}' (+2.0)")
    else:
        reasons.append(f"mood: no match ('{user_prefs.get('mood')}' ≠ '{song['mood']}') (+0.0)")

    # --- Categorical: genre (+1.5 exact match, else +0.0) ---
    if user_prefs.get("genre") == song["genre"]:
        score += 1.5
        reasons.append(f"genre match: '{song['genre']}' (+1.5)")
    else:
        reasons.append(f"genre: no match ('{user_prefs.get('genre')}' ≠ '{song['genre']}') (+0.0)")

    # --- Numeric: energy (+2.0 max) ---
    energy_pts = 2.0 * (1 - abs(user_prefs.get("energy", 0.5) - song["energy"]))
    score += energy_pts
    reasons.append(f"energy {song['energy']:.2f} vs target {user_prefs.get('energy', 0.5):.2f} (+{energy_pts:.2f})")

    # --- Numeric: valence (+1.5 max) ---
    valence_pts = 1.5 * (1 - abs(user_prefs.get("target_valence", 0.5) - song["valence"]))
    score += valence_pts
    reasons.append(f"valence {song['valence']:.2f} vs target {user_prefs.get('target_valence', 0.5):.2f} (+{valence_pts:.2f})")

    # --- Numeric: acousticness (+1.0 max) ---
    target_acousticness = 0.78 if user_prefs.get("likes_acoustic", False) else 0.18
    acousticness_pts = 1.0 * (1 - abs(target_acousticness - song["acousticness"]))
    score += acousticness_pts
    reasons.append(f"acousticness {song['acousticness']:.2f} vs target {target_acousticness:.2f} (+{acousticness_pts:.2f})")

    # --- Numeric: danceability (+0.8 max) ---
    dance_pts = 0.8 * (1 - abs(user_prefs.get("target_danceability", 0.5) - song["danceability"]))
    score += dance_pts
    reasons.append(f"danceability {song['danceability']:.2f} vs target {user_prefs.get('target_danceability', 0.5):.2f} (+{dance_pts:.2f})")

    # --- Numeric: speechiness (+0.5 max) ---
    speech_pts = 0.5 * (1 - abs(user_prefs.get("target_speechiness", 0.05) - song["speechiness"]))
    score += speech_pts
    reasons.append(f"speechiness {song['speechiness']:.2f} vs target {user_prefs.get('target_speechiness', 0.05):.2f} (+{speech_pts:.2f})")

    # --- Numeric: instrumentalness (+0.5 max) ---
    instr_pts = 0.5 * (1 - abs(user_prefs.get("target_instrumentalness", 0.30) - song["instrumentalness"]))
    score += instr_pts
    reasons.append(f"instrumentalness {song['instrumentalness']:.2f} vs target {user_prefs.get('target_instrumentalness', 0.30):.2f} (+{instr_pts:.2f})")

    # --- Numeric: tempo (+0.2 max, normalized to 0–1 before comparison) ---
    song_tempo_norm = (song["tempo_bpm"] - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN)
    user_tempo_norm = (user_prefs.get("target_tempo_bpm", 100.0) - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN)
    tempo_pts = 0.2 * (1 - abs(user_tempo_norm - song_tempo_norm))
    score += tempo_pts
    reasons.append(f"tempo {song['tempo_bpm']:.0f} BPM vs target {user_prefs.get('target_tempo_bpm', 100.0):.0f} BPM (+{tempo_pts:.2f})")

    # --- New: mood tags (up to 3 matching tags × 0.5 = max 1.5) ---
    user_tags = set(user_prefs.get("desired_mood_tags", []))
    song_tags = set(song.get("mood_tags", []))
    if user_tags:
        matches = user_tags & song_tags
        tag_pts = min(len(matches), 3) * 0.5
        score += tag_pts
        match_str = ", ".join(sorted(matches)) if matches else "none"
        reasons.append(f"mood tags matched: [{match_str}] (+{tag_pts:.2f})")
    else:
        reasons.append("mood tags: not specified (+0.00)")

    # --- New: popularity (max 0.8) ---
    # "mainstream" rewards high popularity, "underground" rewards low,
    # "neutral" uses proximity to a target value.
    pop_pref = user_prefs.get("popularity_preference", "neutral")
    song_pop = song.get("popularity", 50)
    if pop_pref == "mainstream":
        pop_pts = 0.8 * (song_pop / 100)
        reasons.append(f"popularity {song_pop}/100 — mainstream preference (+{pop_pts:.2f})")
    elif pop_pref == "underground":
        pop_pts = 0.8 * (1 - song_pop / 100)
        reasons.append(f"popularity {song_pop}/100 — underground preference (+{pop_pts:.2f})")
    else:
        target_pop = user_prefs.get("target_popularity", 50)
        pop_pts = 0.8 * (1 - abs(target_pop - song_pop) / 100)
        reasons.append(f"popularity {song_pop}/100 vs target {int(target_pop)}/100 (+{pop_pts:.2f})")
    score += pop_pts

    # --- New: release decade (max 0.7; penalty of 0.25 per decade away, floor at 0) ---
    target_decade = user_prefs.get("target_decade", 2010)
    song_decade = song.get("release_decade", 2010)
    decade_gap = abs(target_decade - song_decade) / 10
    decade_pts = max(0.0, 0.7 * (1.0 - 0.25 * decade_gap))
    score += decade_pts
    reasons.append(f"decade: {song_decade}s vs target {target_decade}s (+{decade_pts:.2f})")

    # --- New: liveness (max 0.4) ---
    liveness_pts = 0.4 * (1 - abs(user_prefs.get("target_liveness", 0.15) - song.get("liveness", 0.10)))
    score += liveness_pts
    reasons.append(f"liveness {song.get('liveness', 0.10):.2f} vs target {user_prefs.get('target_liveness', 0.15):.2f} (+{liveness_pts:.2f})")

    # --- New: explicit filter (max 0.3; blocked if user disallows explicit content) ---
    allow_explicit = user_prefs.get("allow_explicit", True)
    is_explicit = bool(song.get("explicit", 0))
    if not allow_explicit and is_explicit:
        reasons.append("explicit: content blocked by user preference (+0.00)")
    else:
        score += 0.3
        label = "explicit" if is_explicit else "clean"
        reasons.append(f"explicit: {label} — permitted (+0.30)")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song in the catalog and return the top k as (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, " | ".join(reasons)))

    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
