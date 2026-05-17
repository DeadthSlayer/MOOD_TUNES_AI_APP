import asyncio
import html
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from backend.app.spotify import MoodNotFoundError, SpotifyClient, mood_catalog


ROOT_DIR = Path(__file__).resolve().parent
load_dotenv(ROOT_DIR / ".env")

MOOD_STYLES = {
    "happy": {"icon": "😊", "gradient": "linear-gradient(135deg, #fde047, #84cc16, #22c55e)"},
    "sad": {"icon": "💧", "gradient": "linear-gradient(135deg, #38bdf8, #6366f1, #8b5cf6)"},
    "angry": {"icon": "🔥", "gradient": "linear-gradient(135deg, #ef4444, #f97316, #f59e0b)"},
    "calm": {"icon": "🌙", "gradient": "linear-gradient(135deg, #2dd4bf, #22d3ee, #3b82f6)"},
    "energetic": {"icon": "⚡", "gradient": "linear-gradient(135deg, #d946ef, #8b5cf6, #22d3ee)"},
    "romantic": {"icon": "💗", "gradient": "linear-gradient(135deg, #fb7185, #ec4899, #a855f7)"},
    "focused": {"icon": "🎯", "gradient": "linear-gradient(135deg, #6ee7b7, #22c55e, #22d3ee)"},
    "lonely": {"icon": "🌌", "gradient": "linear-gradient(135deg, #94a3b8, #3b82f6, #4f46e5)"},
    "motivated": {"icon": "🚀", "gradient": "linear-gradient(135deg, #fdba74, #a3e635, #22c55e)"},
    "chill": {"icon": "🫧", "gradient": "linear-gradient(135deg, #67e8f9, #38bdf8, #6ee7b7)"},
}


def run_async(coro):
    """Run async Spotify calls from Streamlit's synchronous script runtime."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@st.cache_data(ttl=600, show_spinner=False)
def fetch_recommendations(mood: str, limit: int = 12):
    client = SpotifyClient()
    return run_async(client.recommend_for_mood(mood, limit=limit))


def inject_css():
    st.markdown(
        """
        <style>
        :root {
            --spotify: #1ed760;
        }

        .stApp {
            background:
                radial-gradient(circle at 10% 10%, rgba(30, 215, 96, .18), transparent 30rem),
                radial-gradient(circle at 90% 4%, rgba(59, 130, 246, .22), transparent 28rem),
                radial-gradient(circle at 50% 100%, rgba(236, 72, 153, .16), transparent 32rem),
                #05070d;
            color: #f8fafc;
        }

        .block-container {
            max-width: 1180px;
            padding-top: 2.5rem;
            padding-bottom: 4rem;
        }

        [data-testid="stHeader"] {
            background: rgba(5, 7, 13, .72);
            backdrop-filter: blur(18px);
        }

        .hero {
            border: 1px solid rgba(255, 255, 255, .12);
            border-radius: 18px;
            background: linear-gradient(145deg, rgba(15, 23, 42, .78), rgba(15, 23, 42, .38));
            box-shadow: 0 24px 90px rgba(0, 0, 0, .32);
            padding: clamp(1.5rem, 5vw, 3.5rem);
            overflow: hidden;
            position: relative;
        }

        .hero:before {
            content: "";
            position: absolute;
            inset: -40%;
            background: conic-gradient(from 180deg, rgba(30, 215, 96, .22), rgba(59, 130, 246, .2), rgba(236, 72, 153, .18), rgba(30, 215, 96, .22));
            filter: blur(70px);
            opacity: .55;
            animation: drift 18s ease-in-out infinite alternate;
        }

        .hero > * {
            position: relative;
            z-index: 1;
        }

        @keyframes drift {
            from { transform: translate3d(-4%, -2%, 0) rotate(0deg) scale(1); }
            to { transform: translate3d(4%, 3%, 0) rotate(16deg) scale(1.08); }
        }

        .eyebrow {
            display: inline-flex;
            border: 1px solid rgba(110, 231, 183, .28);
            border-radius: 10px;
            background: rgba(16, 185, 129, .12);
            color: #d1fae5;
            font-weight: 800;
            padding: .55rem .9rem;
            margin-bottom: 1rem;
        }

        .hero h1 {
            font-size: clamp(3.25rem, 9vw, 6.8rem);
            line-height: .92;
            letter-spacing: 0;
            margin: 0;
        }

        .hero p {
            max-width: 760px;
            color: #cbd5e1;
            font-size: 1.08rem;
            line-height: 1.8;
            margin-top: 1.2rem;
        }

        div.stButton > button {
            width: 100%;
            min-height: 5.25rem;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, .14);
            background: rgba(15, 23, 42, .56);
            color: white;
            font-weight: 800;
            font-size: 1.08rem;
            box-shadow: 0 18px 60px rgba(0, 0, 0, .22);
            transition: transform .18s ease, border-color .18s ease, box-shadow .18s ease;
        }

        div.stButton > button:hover {
            transform: translateY(-4px);
            border-color: rgba(30, 215, 96, .72);
            box-shadow: 0 0 34px rgba(30, 215, 96, .24);
        }

        .track-card {
            border: 1px solid rgba(255, 255, 255, .12);
            border-radius: 14px;
            background: linear-gradient(145deg, rgba(15, 23, 42, .78), rgba(15, 23, 42, .38));
            box-shadow: 0 18px 60px rgba(0, 0, 0, .28);
            padding: 1rem;
            height: 100%;
        }

        .track-card img {
            width: 100%;
            aspect-ratio: 1;
            object-fit: cover;
            border-radius: 12px;
            margin-bottom: 1rem;
        }

        .track-title {
            font-weight: 900;
            font-size: 1.08rem;
            margin-bottom: .2rem;
        }

        .track-meta {
            color: #cbd5e1;
            font-size: .92rem;
            margin-bottom: .2rem;
        }

        .track-album {
            color: #94a3b8;
            font-size: .75rem;
            text-transform: uppercase;
            letter-spacing: .18em;
            min-height: 2.2rem;
        }

        .spotify-link {
            display: inline-flex;
            justify-content: center;
            width: 100%;
            border-radius: 10px;
            background: var(--spotify);
            color: #020617 !important;
            font-weight: 900;
            text-decoration: none;
            padding: .75rem 1rem;
            margin-top: .9rem;
        }

        .status-pill {
            display: inline-flex;
            border-radius: 10px;
            border: 1px solid rgba(251, 191, 36, .28);
            background: rgba(251, 191, 36, .1);
            color: #fde68a;
            padding: .65rem .9rem;
            font-weight: 700;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero():
    st.markdown(
        """
        <section class="hero">
            <span class="eyebrow">Spotify-powered mood recommendations</span>
            <h1>MoodTune AI</h1>
            <p>
                Choose your current mood and the recommendation engine maps it to genres,
                searches Spotify, and returns album art, artists, preview audio when available,
                and direct Spotify links. No webcam. No facial recognition.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def mood_picker():
    st.subheader("Select your current frequency")
    catalog = mood_catalog()
    mood_items = list(catalog.items())

    for row_start in range(0, len(mood_items), 5):
        columns = st.columns(5)
        for column, (mood_id, profile) in zip(columns, mood_items[row_start : row_start + 5]):
            with column:
                style = MOOD_STYLES[mood_id]
                st.markdown(
                    f"""
                    <div style="
                        min-height: 8.75rem;
                        border-radius: 14px;
                        border: 1px solid rgba(255,255,255,.15);
                        background: {style['gradient']};
                        box-shadow: 0 20px 60px rgba(0,0,0,.28);
                        padding: 1rem;
                        margin-bottom: .55rem;
                        color: #020617;
                        display: flex;
                        flex-direction: column;
                        justify-content: space-between;
                    ">
                        <div style="font-size:2rem;">{style['icon']}</div>
                        <div>
                            <div style="font-weight:900;font-size:1.25rem;">{profile['label']}</div>
                            <div style="font-weight:700;font-size:.78rem;opacity:.78;">{", ".join(profile["genres"])}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button(
                    f"Tune {profile['label']}",
                    key=f"mood-{mood_id}",
                    help=f"Genres: {', '.join(profile['genres'])}",
                ):
                    st.session_state["selected_mood"] = mood_id


def render_recommendations(mood_id: str):
    profile = mood_catalog()[mood_id]
    style = MOOD_STYLES[mood_id]

    st.markdown("---")
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:.75rem;flex-wrap:wrap;margin-bottom:.35rem;">
            <span style="background:{style['gradient']};color:#020617;border-radius:10px;padding:.55rem .85rem;font-weight:900;">
                {style['icon']} {profile['label']}
            </span>
            <span style="color:#cbd5e1;">Genres: {", ".join(profile["genres"])}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    try:
        with st.spinner("Tuning the recommendation engine..."):
            data = fetch_recommendations(mood_id)
    except MoodNotFoundError as error:
        st.error(str(error))
        return
    except Exception as error:
        st.error(f"Could not fetch recommendations: {error}")
        return

    if data.get("source") == "demo":
        st.markdown(
            '<span class="status-pill">Demo mode: add Spotify credentials for live tracks.</span>',
            unsafe_allow_html=True,
        )

    tracks = data.get("tracks", [])
    for row_start in range(0, len(tracks), 3):
        columns = st.columns(3)
        for column, track in zip(columns, tracks[row_start : row_start + 3]):
            with column:
                render_track(track)


def render_track(track):
    image = track.get("image") or "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=900&q=80"
    spotify_url = track.get("spotifyUrl") or "https://open.spotify.com"
    title = html.escape(track.get("title", "Untitled"))
    artist = html.escape(track.get("artist", "Unknown Artist"))
    album = html.escape(track.get("album", "Single"))
    image_alt = html.escape(f"{track.get('album', 'Album')} album artwork")

    st.markdown(
        f"""
        <article class="track-card">
            <img src="{image}" alt="{image_alt}" />
            <div class="track-title">{title}</div>
            <div class="track-meta">{artist}</div>
            <div class="track-album">{album}</div>
        """,
        unsafe_allow_html=True,
    )

    if track.get("previewUrl"):
        st.audio(track["previewUrl"])
    else:
        st.caption("Preview unavailable")

    st.markdown(
        f'<a class="spotify-link" href="{spotify_url}" target="_blank" rel="noreferrer">Open in Spotify</a></article>',
        unsafe_allow_html=True,
    )


def main():
    st.set_page_config(
        page_title="MoodTune AI",
        page_icon="🎧",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    inject_css()
    hero()
    st.write("")
    mood_picker()

    selected_mood = st.session_state.get("selected_mood")
    if selected_mood:
        render_recommendations(selected_mood)
    else:
        st.info("Pick a mood above to generate your playlist signal.")


if __name__ == "__main__":
    main()
