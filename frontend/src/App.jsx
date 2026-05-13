import { useEffect, useState } from "react";

const api = (path) => fetch(`/api${path}`).then((r) => r.json());

export default function App() {
  const [health, setHealth] = useState(null);
  const [db, setDb] = useState(null);
  const [err, setErr] = useState(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const [h, d] = await Promise.all([api("/health"), api("/db-check")]);
        if (!cancelled) {
          setHealth(h);
          setDb(d);
        }
      } catch (e) {
        if (!cancelled) setErr(String(e));
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <main style={{ fontFamily: "system-ui", padding: "2rem", maxWidth: 480 }}>
      <h1 style={{ marginTop: 0 }}>React + FastAPI + Postgres</h1>
      {err && <p style={{ color: "crimson" }}>{err}</p>}
      <pre style={{ background: "#f4f4f5", padding: "1rem", borderRadius: 8 }}>
        {JSON.stringify({ health, db }, null, 2)}
      </pre>
      <p style={{ color: "#71717a", fontSize: 14 }}>
        Локально: <code>npm run dev</code> — запросы идут на FastAPI через прокси{" "}
        <code>/api</code>.
      </p>
    </main>
  );
}
