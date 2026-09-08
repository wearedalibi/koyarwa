# Koyarwa

Projet full-stack : API **FastAPI** (Python/uv) + client **React + Fluent UI**.

```
koyarwa/
├── backend/            # API FastAPI (uv) — architecture vertical slice
├── portal/             # SPA React + Fluent UI (Vite)
└── docker-compose.yml  # Postgres + API (le portal se lance en local)
```

## Démarrage rapide

### 1. Base de données (optionnel — requis pour les features qui persistent)

```bash
docker compose up -d db
```

### 2. Backend

```bash
cd backend
cp .env.example .env
uv sync
uv run uvicorn koyarwa.main:app --reload
```

API sur http://localhost:8000 · docs sur http://localhost:8000/docs

### 3. Portal

```bash
cd portal
cp .env.example .env
npm install
npm run dev
```

App sur http://localhost:5173

Voir [`backend/README.md`](backend/README.md) et [`portal/README.md`](portal/README.md)
pour le détail.
