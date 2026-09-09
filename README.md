# Koyarwa

**Koyarwa** — plateforme d'apprentissage en ligne (LMS) open source, déployée **en
instance par établissement**. API **FastAPI** (Python/uv) + espace d'administration +
portail **React / Fluent UI**.

```
koyarwa/
├── backend/            # API + espace d'administration (FastAPI, uv)
├── portal/             # portail React + Fluent UI (Vite, servi par nginx en prod)
├── docs/               # documentation (site MkDocs)
└── docker-compose.yml  # base + backend + portal
```

## Documentation

La documentation complète est dans [`docs/`](docs/index.md) — vue d'ensemble, concepts,
architecture, mise en place, administration, modèle de données, API et feuille de route.

```bash
uv tool run --with mkdocs-material mkdocs serve -a localhost:8081
```

## Tout via Docker

Chaque projet a son `Dockerfile` (backend : uv → uvicorn ; portal : build Vite
servi par **nginx**, avec proxy `/api` vers le backend). Pour tout lancer :

```bash
docker compose up --build
```

- Portal : http://localhost:3000  (nginx sert la SPA et proxifie `/api`)
- API : http://localhost:8000  ·  docs : http://localhost:8000/docs

## Développement local (hot reload)

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
