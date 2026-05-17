const { useEffect, useMemo, useState } = React;
const motionLib = window.Motion || window.FramerMotion || {};
// The app prefers Framer Motion, but this fallback prevents a blank page if a CDN is blocked.
const fallbackMotion = new Proxy({}, {
  get: (_, tag) => React.forwardRef((props, ref) => {
    const {
      initial,
      animate,
      exit,
      transition,
      whileInView,
      viewport,
      whileHover,
      whileTap,
      ...safeProps
    } = props;
    return React.createElement(tag, { ...safeProps, ref }, props.children);
  }),
});
const motion = motionLib.motion || fallbackMotion;
const AnimatePresence = motionLib.AnimatePresence || (({ children }) => React.createElement(React.Fragment, null, children));

const api = axios.create({ baseURL: "" });

const moodCards = [
  { id: "happy", label: "Happy", icon: "😊", pulse: "from-yellow-300 via-lime-300 to-emerald-400", glow: "rgba(250, 204, 21, .34)" },
  { id: "sad", label: "Sad", icon: "💧", pulse: "from-sky-400 via-indigo-400 to-violet-500", glow: "rgba(56, 189, 248, .32)" },
  { id: "angry", label: "Angry", icon: "🔥", pulse: "from-red-500 via-orange-500 to-amber-400", glow: "rgba(239, 68, 68, .36)" },
  { id: "calm", label: "Calm", icon: "🌙", pulse: "from-teal-300 via-cyan-400 to-blue-500", glow: "rgba(45, 212, 191, .32)" },
  { id: "energetic", label: "Energetic", icon: "⚡", pulse: "from-fuchsia-500 via-purple-500 to-cyan-400", glow: "rgba(217, 70, 239, .34)" },
  { id: "romantic", label: "Romantic", icon: "💗", pulse: "from-rose-400 via-pink-500 to-purple-500", glow: "rgba(244, 114, 182, .34)" },
  { id: "focused", label: "Focused", icon: "🎯", pulse: "from-emerald-300 via-green-400 to-cyan-400", glow: "rgba(52, 211, 153, .32)" },
  { id: "lonely", label: "Lonely", icon: "🌌", pulse: "from-slate-400 via-blue-500 to-indigo-600", glow: "rgba(99, 102, 241, .3)" },
  { id: "motivated", label: "Motivated", icon: "🚀", pulse: "from-orange-300 via-lime-400 to-green-400", glow: "rgba(132, 204, 22, .34)" },
  { id: "chill", label: "Chill", icon: "🫧", pulse: "from-cyan-300 via-sky-400 to-emerald-300", glow: "rgba(125, 211, 252, .32)" },
];

function App() {
  const [route, setRoute] = useState(() => window.location.pathname);

  useEffect(() => {
    const onPop = () => setRoute(window.location.pathname);
    window.addEventListener("popstate", onPop);
    return () => window.removeEventListener("popstate", onPop);
  }, []);

  const navigate = (path) => {
    // Tiny client router so no Node-based bundler or React Router install is required.
    window.history.pushState({}, "", path);
    setRoute(path);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const match = route.match(/^\/recommendations\/([^/]+)/);
  const selectedMood = match ? decodeURIComponent(match[1]) : null;

  return (
    <Shell navigate={navigate}>
      <AnimatePresence mode="wait">
        {selectedMood ? (
          <Recommendations key={selectedMood} mood={selectedMood} navigate={navigate} />
        ) : (
          <Home key="home" navigate={navigate} />
        )}
      </AnimatePresence>
    </Shell>
  );
}

function Shell({ children, navigate }) {
  return (
    <main className="relative min-h-screen overflow-hidden">
      <div className="aurora" aria-hidden="true" />
      <div className="animated-grid pointer-events-none absolute inset-0" aria-hidden="true" />
      <nav className="relative z-20 mx-auto flex max-w-7xl items-center justify-between px-5 py-5 sm:px-8">
        <button onClick={() => navigate("/")} className="flex items-center gap-3 text-left">
          <span className="grid h-11 w-11 place-items-center rounded-lg bg-emerald-400 text-xl text-slate-950 shadow-neon">♪</span>
          <span>
            <span className="block font-display text-lg font-bold">MoodTune AI</span>
            <span className="block text-xs uppercase tracking-[.28em] text-emerald-200/70">Neural playlists</span>
          </span>
        </button>
        <a href="/health" className="hidden rounded-lg border border-white/10 px-4 py-2 text-sm text-slate-200 transition hover:border-emerald-300/70 hover:text-white sm:inline-flex">
          API Health
        </a>
      </nav>
      <div className="relative z-10">{children}</div>
    </main>
  );
}

function Home({ navigate }) {
  return (
    <motion.section
      initial={{ opacity: 0, y: 18 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -18 }}
      transition={{ duration: .45 }}
      className="mx-auto max-w-7xl px-5 pb-16 pt-8 sm:px-8"
    >
      <section className="grid min-h-[64vh] items-center gap-10 py-8 lg:grid-cols-[1.05fr_.95fr]">
        <div>
          <motion.div
            initial={{ opacity: 0, scale: .92 }}
            animate={{ opacity: 1, scale: 1 }}
            className="mb-6 inline-flex rounded-lg border border-emerald-300/20 bg-emerald-300/10 px-4 py-2 text-sm font-semibold text-emerald-100"
          >
            Spotify-powered mood recommendations
          </motion.div>
          <h1 className="max-w-4xl font-display text-5xl font-bold leading-tight text-white sm:text-7xl">
            MoodTune AI
          </h1>
          <p className="mt-6 max-w-2xl text-lg leading-8 text-slate-300">
            Pick how you feel and let the recommendation engine translate that signal into dynamic music, album art, previews, and Spotify links.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <button onClick={() => document.querySelector("#moods").scrollIntoView({ behavior: "smooth" })} className="rounded-lg bg-emerald-400 px-6 py-3 font-bold text-slate-950 shadow-neon transition hover:bg-emerald-300">
              Choose a mood
            </button>
            <button onClick={() => navigate("/recommendations/chill")} className="rounded-lg border border-white/15 px-6 py-3 font-bold text-white transition hover:border-cyan-300/80 hover:bg-white/10">
              Surprise me
            </button>
          </div>
        </div>

        <motion.div
          initial={{ opacity: 0, rotateX: 12, y: 24 }}
          animate={{ opacity: 1, rotateX: 0, y: 0 }}
          transition={{ delay: .15, duration: .6 }}
          className="glass relative overflow-hidden rounded-lg p-5"
        >
          <div className="absolute right-4 top-4 h-3 w-3 rounded-full bg-emerald-300 shadow-neon" />
          <div className="rounded-lg border border-white/10 bg-black/20 p-4">
            <div className="mb-4 h-2 w-36 rounded-full bg-emerald-300/80" />
            <div className="space-y-3">
              {["Mood vector", "Genre mapping", "Spotify search", "Preview stream"].map((item, index) => (
                <motion.div
                  key={item}
                  animate={{ opacity: [0.55, 1, 0.55] }}
                  transition={{ duration: 2.4, delay: index * .25, repeat: Infinity }}
                  className="flex items-center justify-between rounded-lg border border-white/10 bg-white/[.04] px-4 py-3"
                >
                  <span className="text-sm text-slate-300">{item}</span>
                  <span className="h-2 w-20 rounded-full bg-gradient-to-r from-emerald-300 to-cyan-300" />
                </motion.div>
              ))}
            </div>
          </div>
        </motion.div>
      </section>

      <section id="moods" className="pt-10">
        <div className="mb-6 flex flex-col justify-between gap-3 sm:flex-row sm:items-end">
          <div>
            <h2 className="font-display text-3xl font-bold">Select your current frequency</h2>
            <p className="mt-2 text-slate-300">No camera, no facial recognition. Just tap the mood that fits.</p>
          </div>
        </div>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
          {moodCards.map((mood, index) => (
            <MoodCard key={mood.id} mood={mood} index={index} onSelect={() => navigate(`/recommendations/${mood.id}`)} />
          ))}
        </div>
      </section>
    </motion.section>
  );
}

function MoodCard({ mood, index, onSelect }) {
  return (
    <motion.button
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-40px" }}
      transition={{ delay: index * .035 }}
      whileHover={{ y: -8, scale: 1.03 }}
      whileTap={{ scale: .98 }}
      onClick={onSelect}
      className="group relative min-h-44 overflow-hidden rounded-lg border border-white/10 bg-slate-950/50 p-5 text-left backdrop-blur-xl"
      style={{ boxShadow: `0 0 0 rgba(0,0,0,0)` }}
    >
      <div className={`absolute inset-0 bg-gradient-to-br ${mood.pulse} opacity-[.18] transition duration-300 group-hover:opacity-[.35]`} />
      <div className="absolute inset-x-5 bottom-0 h-16 rounded-full blur-3xl transition duration-300 group-hover:opacity-100" style={{ background: mood.glow, opacity: .48 }} />
      <div className="relative">
        <span className="mb-7 grid h-14 w-14 place-items-center rounded-lg bg-black/30 text-3xl ring-1 ring-white/15">
          {mood.icon}
        </span>
        <h3 className="font-display text-2xl font-bold text-white">{mood.label}</h3>
        <p className="mt-2 text-sm text-slate-200/80">Generate a playlist signal</p>
      </div>
    </motion.button>
  );
}

function Recommendations({ mood, navigate }) {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const moodMeta = useMemo(() => moodCards.find((item) => item.id === mood) || moodCards[0], [mood]);

  useEffect(() => {
    setLoading(true);
    setError("");
    api.get(`/recommend/${mood}`)
      .then((response) => setData(response.data))
      .catch(() => setError("The recommendation engine is offline. Check the FastAPI server and Spotify credentials."))
      .finally(() => setLoading(false));
  }, [mood]);

  return (
    <motion.section
      initial={{ opacity: 0, y: 18 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -18 }}
      transition={{ duration: .45 }}
      className="mx-auto max-w-7xl px-5 pb-16 pt-8 sm:px-8"
    >
      <button onClick={() => navigate("/")} className="mb-6 rounded-lg border border-white/15 px-4 py-2 text-sm font-semibold text-slate-200 transition hover:border-emerald-300/80 hover:text-white">
        Back to moods
      </button>

      <div className="mb-8 flex flex-col gap-5 rounded-lg border border-white/10 bg-black/20 p-5 backdrop-blur-xl sm:flex-row sm:items-center sm:justify-between">
        <div>
          <div className={`mb-4 inline-flex rounded-lg bg-gradient-to-r ${moodMeta.pulse} px-4 py-2 font-bold text-slate-950`}>
            {moodMeta.icon} {data?.label || moodMeta.label}
          </div>
          <h1 className="font-display text-4xl font-bold sm:text-5xl">Recommendations</h1>
          <p className="mt-3 max-w-2xl text-slate-300">
            Genres: {(data?.genres || []).join(", ") || "loading signal"}
          </p>
        </div>
        {data?.source === "demo" && (
          <span className="rounded-lg border border-amber-300/30 bg-amber-300/10 px-4 py-3 text-sm text-amber-100">
            Demo mode: add Spotify credentials for live tracks.
          </span>
        )}
      </div>

      {loading && <LoadingGrid />}
      {error && <ErrorState message={error} />}
      {!loading && !error && (
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {(data?.tracks || []).map((track, index) => (
            <TrackCard key={`${track.title}-${index}`} track={track} index={index} />
          ))}
        </div>
      )}
    </motion.section>
  );
}

function LoadingGrid() {
  return (
    <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      {Array.from({ length: 8 }).map((_, index) => (
        <div key={index} className="glass h-80 animate-pulse rounded-lg p-4">
          <div className="h-44 rounded-lg bg-white/10" />
          <div className="mt-5 h-4 w-3/4 rounded bg-white/10" />
          <div className="mt-3 h-3 w-1/2 rounded bg-white/10" />
        </div>
      ))}
    </div>
  );
}

function ErrorState({ message }) {
  return (
    <div className="rounded-lg border border-red-300/30 bg-red-500/10 p-5 text-red-100">
      {message}
    </div>
  );
}

function TrackCard({ track, index }) {
  return (
    <motion.article
      initial={{ opacity: 0, y: 18 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * .04 }}
      className="glass group overflow-hidden rounded-lg p-4"
    >
      <div className="relative aspect-square overflow-hidden rounded-lg bg-slate-900">
        <img
          src={track.image || "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=900&q=80"}
          alt={`${track.album} album artwork`}
          className="h-full w-full object-cover transition duration-500 group-hover:scale-105"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/55 to-transparent" />
      </div>
      <div className="pt-4">
        <h2 className="line-clamp-1 font-display text-xl font-bold">{track.title}</h2>
        <p className="line-clamp-1 mt-1 text-sm text-slate-300">{track.artist}</p>
        <p className="line-clamp-1 mt-1 text-xs uppercase tracking-[.22em] text-slate-500">{track.album}</p>
      </div>
      <div className="mt-4">
        {track.previewUrl ? (
          <audio className="audio-player" controls src={track.previewUrl} />
        ) : (
          <div className="rounded-lg border border-white/10 bg-white/[.04] px-3 py-2 text-sm text-slate-400">
            Preview unavailable
          </div>
        )}
      </div>
      <a
        href={track.spotifyUrl || "https://open.spotify.com"}
        target="_blank"
        rel="noreferrer"
        className="mt-4 flex justify-center rounded-lg bg-emerald-400 px-4 py-3 font-bold text-slate-950 transition hover:bg-emerald-300"
      >
        Open in Spotify
      </a>
    </motion.article>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
