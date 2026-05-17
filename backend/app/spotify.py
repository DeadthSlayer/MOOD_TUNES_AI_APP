import base64
import os
from dataclasses import dataclass
from typing import Any

import httpx


class MoodNotFoundError(ValueError):
    pass


@dataclass(frozen=True)
class MoodProfile:
    label: str
    query: str
    genres: tuple[str, ...]
    market: str = "US"


MOOD_PROFILES: dict[str, MoodProfile] = {
    "happy": MoodProfile("Happy", "happy pop dance feel good", ("pop", "dance", "disco")),
    "sad": MoodProfile("Sad", "sad acoustic soft piano", ("acoustic", "singer-songwriter", "piano")),
    "angry": MoodProfile("Angry", "angry rock metal workout", ("rock", "metal", "hard-rock")),
    "calm": MoodProfile("Calm", "calm lofi ambient instrumental", ("lofi", "ambient", "chill")),
    "energetic": MoodProfile("Energetic", "energetic edm workout", ("edm", "workout", "electronic")),
    "romantic": MoodProfile("Romantic", "romantic rnb love songs", ("r-n-b", "soul", "pop")),
    "focused": MoodProfile("Focused", "focus deep work instrumental electronic", ("study", "ambient", "minimal-techno")),
    "lonely": MoodProfile("Lonely", "lonely indie acoustic night", ("indie", "acoustic", "folk")),
    "motivated": MoodProfile("Motivated", "motivational hip hop pop workout", ("hip-hop", "pop", "workout")),
    "chill": MoodProfile("Chill", "chill lofi lounge relaxed", ("chill", "lofi", "lounge")),
}


DEMO_TRACKS = [
    {
        "title": "Neon Skyline",
        "artist": "MoodTune Studio",
        "album": "Synthetic Feelings",
        "image": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?auto=format&fit=crop&w=900&q=80",
        "previewUrl": None,
        "spotifyUrl": "https://open.spotify.com",
    },
    {
        "title": "Pulse Atlas",
        "artist": "Aurora Circuit",
        "album": "Signals",
        "image": "https://images.unsplash.com/photo-1511379938547-c1f69419868d?auto=format&fit=crop&w=900&q=80",
        "previewUrl": None,
        "spotifyUrl": "https://open.spotify.com",
    },
    {
        "title": "Glass Heart",
        "artist": "Violet Echo",
        "album": "Afterglow",
        "image": "https://images.unsplash.com/photo-1516280440614-37939bbacd81?auto=format&fit=crop&w=900&q=80",
        "previewUrl": None,
        "spotifyUrl": "https://open.spotify.com",
    },
]


def mood_catalog() -> dict[str, dict[str, Any]]:
    return {
        key: {
            "label": profile.label,
            "genres": profile.genres,
            "query": profile.query,
        }
        for key, profile in MOOD_PROFILES.items()
    }


class SpotifyClient:
    token_url = "https://accounts.spotify.com/api/token"
    search_url = "https://api.spotify.com/v1/search"

    def __init__(self):
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self._access_token: str | None = None

    @property
    def is_configured(self) -> bool:
        return bool(self.client_id and self.client_secret)

    async def recommend_for_mood(self, mood: str, limit: int = 12) -> dict[str, Any]:
        key = mood.lower().strip()
        if key not in MOOD_PROFILES:
            raise MoodNotFoundError(f"Unknown mood '{mood}'.")

        profile = MOOD_PROFILES[key]
        tracks = await self._spotify_search(profile, limit=min(max(limit, 1), 24))

        return {
            "mood": key,
            "label": profile.label,
            "genres": profile.genres,
            "source": "spotify" if self.is_configured and tracks else "demo",
            "tracks": tracks or self._demo_tracks(profile),
        }

    async def _get_token(self) -> str | None:
        # Spotify Client Credentials flow: perfect for app-level search requests.
        if not self.is_configured:
            return None

        if self._access_token:
            return self._access_token

        credentials = f"{self.client_id}:{self.client_secret}".encode("utf-8")
        auth = base64.b64encode(credentials).decode("utf-8")

        try:
            async with httpx.AsyncClient(timeout=12) as client:
                response = await client.post(
                    self.token_url,
                    headers={"Authorization": f"Basic {auth}"},
                    data={"grant_type": "client_credentials"},
                )
                response.raise_for_status()
                payload = response.json()
                self._access_token = payload.get("access_token")
                return self._access_token
        except httpx.HTTPError:
            self._access_token = None
            return None

    async def _spotify_search(self, profile: MoodProfile, limit: int) -> list[dict[str, Any]]:
        token = await self._get_token()
        if not token:
            return []

        params = {
            "q": profile.query,
            "type": "track",
            "market": profile.market,
            "limit": limit,
        }

        try:
            async with httpx.AsyncClient(timeout=12) as client:
                response = await client.get(
                    self.search_url,
                    headers={"Authorization": f"Bearer {token}"},
                    params=params,
                )
                response.raise_for_status()
        except httpx.HTTPStatusError as error:
            if error.response.status_code == 401:
                self._access_token = None
            return []
        except httpx.HTTPError:
            return []

        items = response.json().get("tracks", {}).get("items", [])
        return [self._normalize_track(item) for item in items]

    def _normalize_track(self, item: dict[str, Any]) -> dict[str, Any]:
        album = item.get("album") or {}
        images = album.get("images") or []
        artists = item.get("artists") or []

        return {
            "title": item.get("name", "Untitled"),
            "artist": ", ".join(artist.get("name", "Unknown Artist") for artist in artists),
            "album": album.get("name", "Single"),
            "image": images[0]["url"] if images else None,
            "previewUrl": item.get("preview_url"),
            "spotifyUrl": (item.get("external_urls") or {}).get("spotify"),
        }

    def _demo_tracks(self, profile: MoodProfile) -> list[dict[str, Any]]:
        # Demo tracks make the UI usable before a beginner has Spotify keys.
        return [
            {
                **track,
                "title": f"{profile.label} {track['title']}",
                "artist": f"{track['artist']} - {profile.genres[0].title()} Mix",
            }
            for track in DEMO_TRACKS
        ]
