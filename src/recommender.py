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

# ---------------------------------------------------------------------------
# Ranking strategies — Strategy pattern via weight configurations.
#
# Each entry is a dict of feature → max points. score_song() reads these
# instead of hardcoded numbers, so swapping a strategy changes the entire
# ranking without touching any other logic.
#
# To add a new strategy: add a new key here. No other code needs to change.
# ---------------------------------------------------------------------------
STRATEGY_WEIGHTS: Dict[str, Dict[str, float]] = {
    # Default: all features carry balanced influence.
    "balanced": {
        "mood": 2.0, "genre": 1.5, "energy": 2.0, "valence": 1.5,
        "acousticness": 1.0, "danceability": 0.8, "speechiness": 0.5,
        "instrumentalness": 0.5, "tempo": 0.2,
        "mood_tags": 1.5, "popularity": 0.8, "decade": 0.7,
        "liveness": 0.4, "explicit": 0.3,
    },
    # Genre-First: genre match is the primary filter; everything else is tiebreaker.
    "genre_first": {
        "mood": 0.5, "genre": 5.0, "energy": 1.5, "valence": 1.0,
        "acousticness": 0.7, "danceability": 0.5, "speechiness": 0.3,
        "instrumentalness": 0.3, "tempo": 0.2,
        "mood_tags": 0.5, "popularity": 0.5, "decade": 0.5,
        "liveness": 0.2, "explicit": 0.3,
    },
    # Mood-First: emotional resonance drives the ranking; genre is secondary.
    "mood_first": {
        "mood": 5.0, "genre": 0.5, "energy": 1.0, "valence": 3.0,
        "acousticness": 0.5, "danceability": 0.5, "speechiness": 0.3,
        "instrumentalness": 0.3, "tempo": 0.1,
        "mood_tags": 3.0, "popularity": 0.3, "decade": 0.3,
        "liveness": 0.2, "explicit": 0.3,
    },
    # Energy-Focused: physical intensity (energy, tempo, danceability) dominates.
    "energy_focused": {
        "mood": 0.5, "genre": 0.5, "energy": 5.0, "valence": 1.0,
        "acousticness": 0.8, "danceability": 2.0, "speechiness": 0.3,
        "instrumentalness": 0.3, "tempo": 1.5,
        "mood_tags": 0.3, "popularity": 0.3, "decade": 0.2,
        "liveness": 0.2, "explicit": 0.3,
    },
}


def score_song(user_prefs: Dict, song: Dict,
               weights: Dict = None) -> Tuple[float, List[str]]:
    """Score one song against user preferences and return a list of reasons.

    Pass a custom weights dict or let it default to the 'balanced' strategy.
    Max possible score depends on the active strategy (~10–14 pts).
    """
    W = weights if weights is not None else STRATEGY_WEIGHTS["balanced"]
    TEMPO_MIN, TEMPO_MAX = 60.0, 180.0
    score = 0.0
    reasons = []

    # --- Categorical: mood ---
    if user_prefs.get("mood") == song["mood"]:
        score += W["mood"]
        reasons.append(f"mood match: '{song['mood']}' (+{W['mood']:.1f})")
    else:
        reasons.append(f"mood: no match ('{user_prefs.get('mood')}' ≠ '{song['mood']}') (+0.0)")

    # --- Categorical: genre ---
    if user_prefs.get("genre") == song["genre"]:
        score += W["genre"]
        reasons.append(f"genre match: '{song['genre']}' (+{W['genre']:.1f})")
    else:
        reasons.append(f"genre: no match ('{user_prefs.get('genre')}' ≠ '{song['genre']}') (+0.0)")

    # --- Numeric: energy ---
    energy_pts = W["energy"] * (1 - abs(user_prefs.get("energy", 0.5) - song["energy"]))
    score += energy_pts
    reasons.append(f"energy {song['energy']:.2f} vs target {user_prefs.get('energy', 0.5):.2f} (+{energy_pts:.2f})")

    # --- Numeric: valence ---
    valence_pts = W["valence"] * (1 - abs(user_prefs.get("target_valence", 0.5) - song["valence"]))
    score += valence_pts
    reasons.append(f"valence {song['valence']:.2f} vs target {user_prefs.get('target_valence', 0.5):.2f} (+{valence_pts:.2f})")

    # --- Numeric: acousticness ---
    target_acousticness = 0.78 if user_prefs.get("likes_acoustic", False) else 0.18
    acousticness_pts = W["acousticness"] * (1 - abs(target_acousticness - song["acousticness"]))
    score += acousticness_pts
    reasons.append(f"acousticness {song['acousticness']:.2f} vs target {target_acousticness:.2f} (+{acousticness_pts:.2f})")

    # --- Numeric: danceability ---
    dance_pts = W["danceability"] * (1 - abs(user_prefs.get("target_danceability", 0.5) - song["danceability"]))
    score += dance_pts
    reasons.append(f"danceability {song['danceability']:.2f} vs target {user_prefs.get('target_danceability', 0.5):.2f} (+{dance_pts:.2f})")

    # --- Numeric: speechiness ---
    speech_pts = W["speechiness"] * (1 - abs(user_prefs.get("target_speechiness", 0.05) - song["speechiness"]))
    score += speech_pts
    reasons.append(f"speechiness {song['speechiness']:.2f} vs target {user_prefs.get('target_speechiness', 0.05):.2f} (+{speech_pts:.2f})")

    # --- Numeric: instrumentalness ---
    instr_pts = W["instrumentalness"] * (1 - abs(user_prefs.get("target_instrumentalness", 0.30) - song["instrumentalness"]))
    score += instr_pts
    reasons.append(f"instrumentalness {song['instrumentalness']:.2f} vs target {user_prefs.get('target_instrumentalness', 0.30):.2f} (+{instr_pts:.2f})")

    # --- Numeric: tempo (normalized to 0–1 before comparison) ---
    song_tempo_norm = (song["tempo_bpm"] - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN)
    user_tempo_norm = (user_prefs.get("target_tempo_bpm", 100.0) - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN)
    tempo_pts = W["tempo"] * (1 - abs(user_tempo_norm - song_tempo_norm))
    score += tempo_pts
    reasons.append(f"tempo {song['tempo_bpm']:.0f} BPM vs target {user_prefs.get('target_tempo_bpm', 100.0):.0f} BPM (+{tempo_pts:.2f})")

    # --- New: mood tags (fraction of max weight based on tag overlap, cap 3 matches) ---
    user_tags = set(user_prefs.get("desired_mood_tags", []))
    song_tags = set(song.get("mood_tags", []))
    if user_tags:
        matches = user_tags & song_tags
        tag_pts = (min(len(matches), 3) / 3) * W["mood_tags"]
        score += tag_pts
        match_str = ", ".join(sorted(matches)) if matches else "none"
        reasons.append(f"mood tags matched: [{match_str}] (+{tag_pts:.2f})")
    else:
        reasons.append("mood tags: not specified (+0.00)")

    # --- New: popularity ---
    pop_pref = user_prefs.get("popularity_preference", "neutral")
    song_pop = song.get("popularity", 50)
    if pop_pref == "mainstream":
        pop_pts = W["popularity"] * (song_pop / 100)
        reasons.append(f"popularity {song_pop}/100 — mainstream preference (+{pop_pts:.2f})")
    elif pop_pref == "underground":
        pop_pts = W["popularity"] * (1 - song_pop / 100)
        reasons.append(f"popularity {song_pop}/100 — underground preference (+{pop_pts:.2f})")
    else:
        target_pop = user_prefs.get("target_popularity", 50)
        pop_pts = W["popularity"] * (1 - abs(target_pop - song_pop) / 100)
        reasons.append(f"popularity {song_pop}/100 vs target {int(target_pop)}/100 (+{pop_pts:.2f})")
    score += pop_pts

    # --- New: release decade (penalty of 0.25 per decade away, floor at 0) ---
    target_decade = user_prefs.get("target_decade", 2010)
    song_decade = song.get("release_decade", 2010)
    decade_gap = abs(target_decade - song_decade) / 10
    decade_pts = max(0.0, W["decade"] * (1.0 - 0.25 * decade_gap))
    score += decade_pts
    reasons.append(f"decade: {song_decade}s vs target {target_decade}s (+{decade_pts:.2f})")

    # --- New: liveness ---
    liveness_pts = W["liveness"] * (1 - abs(user_prefs.get("target_liveness", 0.15) - song.get("liveness", 0.10)))
    score += liveness_pts
    reasons.append(f"liveness {song.get('liveness', 0.10):.2f} vs target {user_prefs.get('target_liveness', 0.15):.2f} (+{liveness_pts:.2f})")

    # --- New: explicit filter (hard block if user disallows; otherwise full weight) ---
    allow_explicit = user_prefs.get("allow_explicit", True)
    is_explicit = bool(song.get("explicit", 0))
    if not allow_explicit and is_explicit:
        reasons.append("explicit: content blocked by user preference (+0.00)")
    else:
        score += W["explicit"]
        label = "explicit" if is_explicit else "clean"
        reasons.append(f"explicit: {label} — permitted (+{W['explicit']:.2f})")

    return score, reasons

def _apply_diversity(
    scored: List[Tuple[Dict, float, str]],
    k: int,
    artist_penalty: float,
    genre_penalty: float,
) -> List[Tuple[Dict, float, str]]:
    """Greedy diversity-aware selection.

    Iterates through the pre-sorted scored list and picks songs one slot at a
    time. Each time a song is considered, its effective score is reduced by:
      artist_penalty × (how many times that artist is already in results)
      genre_penalty  × (how many times that genre  is already in results)

    This prevents the same artist or genre from monopolising the top-K list
    without hard-filtering anything out.
    """
    remaining = list(scored)          # mutable copy, sorted by raw score
    selected: List[Tuple[Dict, float, str]] = []
    artist_seen: Dict[str, int] = {}
    genre_seen:  Dict[str, int] = {}

    while len(selected) < k and remaining:
        # Find the candidate with the highest diversity-adjusted score
        def adjusted(item: Tuple) -> float:
            s, score, _ = item
            return (score
                    - artist_seen.get(s["artist"], 0) * artist_penalty
                    - genre_seen.get(s["genre"],  0) * genre_penalty)

        best_idx = max(range(len(remaining)), key=lambda i: adjusted(remaining[i]))
        song, raw_score, explanation = remaining.pop(best_idx)

        penalty = (artist_seen.get(song["artist"], 0) * artist_penalty
                 + genre_seen.get(song["genre"],  0) * genre_penalty)
        adj_score = raw_score - penalty

        if penalty > 0:
            explanation += (f" | diversity penalty: -{penalty:.2f}"
                            f" ({artist_seen.get(song['artist'],0)}× artist,"
                            f" {genre_seen.get(song['genre'],0)}× genre)")

        selected.append((song, adj_score, explanation))
        artist_seen[song["artist"]] = artist_seen.get(song["artist"], 0) + 1
        genre_seen[song["genre"]]   = genre_seen.get(song["genre"],  0) + 1

    return selected


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5,
                    strategy: str = "balanced",
                    artist_penalty: float = 0.0,
                    genre_penalty: float = 0.0) -> List[Tuple[Dict, float, str]]:
    """Score every song in the catalog and return the top k as (song, score, explanation) tuples.

    strategy       — one of 'balanced', 'genre_first', 'mood_first', 'energy_focused'
    artist_penalty — score deducted per additional song from the same artist (e.g. 2.0)
    genre_penalty  — score deducted per additional song from the same genre  (e.g. 1.0)
    Set both to 0.0 (default) to disable diversity enforcement.
    """
    weights = STRATEGY_WEIGHTS.get(strategy, STRATEGY_WEIGHTS["balanced"])
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, weights=weights)
        scored.append((song, score, " | ".join(reasons)))

    scored.sort(key=lambda x: x[1], reverse=True)

    if artist_penalty > 0 or genre_penalty > 0:
        return _apply_diversity(scored, k, artist_penalty, genre_penalty)

    return scored[:k]
