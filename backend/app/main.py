import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from .spotify import MoodNotFoundError, SpotifyClient, mood_catalog


ROOT_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = ROOT_DIR / "frontend"
load_dotenv(ROOT_DIR / ".env")

app = FastAPI(
    title="MoodTune AI",
    description="AI-styled music recommendations powered by moods and Spotify.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

spotify = SpotifyClient()


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "MoodTune AI",
        "spotifyConfigured": spotify.is_configured,
    }


@app.get("/genres")
async def genres():
    return {"moods": mood_catalog()}


@app.get("/recommend/{mood}")
async def recommend(mood: str, limit: int = 12):
    # Keep unknown moods graceful so the frontend can show a friendly empty state.
    try:
        return await spotify.recommend_for_mood(mood, limit=limit)
    except MoodNotFoundError as error:
        return {
            "mood": mood,
            "error": str(error),
            "availableMoods": list(mood_catalog().keys()),
            "tracks": [],
        }


if FRONTEND_DIR.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIR / "assets"), name="assets")


@app.get("/")
async def home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/{full_path:path}")
async def spa_fallback(full_path: str):
    # Serve React routes like /recommendations/happy from the same static app.
    asset_path = FRONTEND_DIR / full_path
    if asset_path.is_file():
        return FileResponse(asset_path)
    return FileResponse(FRONTEND_DIR / "index.html")
