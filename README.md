# MoodTune AI

MoodTune AI is a complete music recommendation app. Users choose a mood from animated cards, and the recommendation engine maps that mood to genres and searches the Spotify Web API for matching tracks.

No webcam, facial recognition, or Node.js build step is used.

## Features

- Futuristic dark glassmorphism UI with animated gradients
- Static React frontend using TailwindCSS, Axios, and Framer Motion from browser CDNs
- Animated mood cards for Happy, Sad, Angry, Calm, Energetic, Romantic, Focused, Lonely, Motivated, and Chill
- FastAPI backend with `/recommend/{mood}`, `/genres`, and `/health`
- Streamlit local app for one-command local hosting
- Spotify Web API integration with album artwork, artists, Spotify links, and preview audio when available
- Demo fallback data when Spotify credentials are not configured
- Responsive mobile-first layout and graceful loading/error states

## Project Structure

```text
MoodTune AI/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── spotify.py
│   └── requirements.txt
├── frontend/
│   ├── assets/
│   │   ├── app.js
│   │   └── styles.css
│   └── index.html
├── streamlit_app.py
├── .env.example
├── package.json
├── requirements.txt
└── README.md
```

## Setup

### Easiest Windows Run

Double-click `run_local.bat`, or run it from PowerShell:

```bash
.\run_local.bat
```

The batch file creates `.venv` if needed, installs dependencies, creates `.env` from `.env.example` if missing, and starts Streamlit at [http://localhost:8501](http://localhost:8501).

### Manual Run

1. Create and activate a Python virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create your environment file:

```bash
copy .env.example .env
```

4. Add Spotify credentials to `.env`:

```env
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
```

5. Start the Streamlit app:

```bash
streamlit run streamlit_app.py
```

6. Open the Streamlit app:

[http://localhost:8501](http://localhost:8501)

## Optional FastAPI + React Version

The original FastAPI-served static React version is still included. Start it with:

```bash
uvicorn backend.app.main:app --reload
```

Then open:

[http://127.0.0.1:8000](http://127.0.0.1:8000)

## Spotify API Setup

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
2. Create an app.
3. Copy the Client ID and Client Secret.
4. Paste them into `.env`.

This app uses Spotify Client Credentials flow, which is suitable for public search-based recommendations and does not require users to log in.

## API Routes

### Health

```http
GET /health
```

Returns service status and whether Spotify credentials are configured.

### Genres

```http
GET /genres
```

Returns the mood-to-genre catalog.

### Recommendations

```http
GET /recommend/{mood}
```

Example:

```http
GET /recommend/happy
```

Returns tracks with title, artist, album, artwork, Spotify URL, and preview URL when Spotify provides one.

## Mood Mapping

- Happy: Pop, Dance, Disco
- Sad: Acoustic, Singer-Songwriter, Piano
- Angry: Rock, Metal, Hard Rock
- Calm: Lofi, Ambient, Chill
- Energetic: EDM, Workout, Electronic
- Romantic: R&B, Soul, Pop
- Focused: Study, Ambient, Minimal Techno
- Lonely: Indie, Acoustic, Folk
- Motivated: Hip-Hop, Pop, Workout
- Chill: Chill, Lofi, Lounge

## Beginner Notes

- The Streamlit app lives in `streamlit_app.py`.
- The shared recommendation engine lives in `backend/app/spotify.py`.
- The optional React frontend lives in `frontend/` and is served by FastAPI.
- `package.json` is included for project metadata only. You do not need to run `npm install`.
- If Spotify credentials are missing, the app still works in demo mode.
