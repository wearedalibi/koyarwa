// Client HTTP minimal vers l'API backend.
// L'URL de base vient de l'environnement Vite (VITE_API_BASE_URL).

const BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";
const API_V1 = `${BASE.replace(/\/$/, "")}/api/v1`;

async function request(path, options) {
  const res = await fetch(`${API_V1}${path}`, options);
  if (!res.ok) {
    throw new Error(`HTTP ${res.status} ${res.statusText}`);
  }
  return res.json();
}

/** GET /api/v1/health → { status, version } */
export function getHealth() {
  return request("/health");
}
