# Installation (développement)

Cette page décrit la mise en route d'un environnement de **développement**. Pour la
mise en place d'une instance destinée à des utilisateurs, voir
[Assistant de mise en place](installeur.md).

## Prérequis

- **Python 3.12+** et [uv](https://docs.astral.sh/uv/)
- **Node.js 20+** et npm
- **PostgreSQL** ou **MySQL** (optionnel au tout début : l'API démarre sans base)
- **Docker** (optionnel, pour le déploiement conteneurisé)

## Arborescence du dépôt

```
koyarwa/
├── backend/            # API + espace d'administration (FastAPI, uv)
├── portal/             # portail web (React + Fluent UI, Vite)
├── docs/               # cette documentation
└── docker-compose.yml  # base + backend + portail
```

## Backend

```bash
cd backend
cp .env.example .env      # ajuster si besoin
uv sync
uv run uvicorn koyarwa.main:app --reload
```

- API : <http://localhost:8000> · documentation OpenAPI : <http://localhost:8000/docs>
- Espace d'administration : <http://localhost:8000/admin>
- Disponibilité : `GET /api/v1/health`

!!! tip "Qualité"
    ```bash
    uv run ruff check .     # lint
    uv run ruff format .    # format
    uv run pytest           # tests
    ```

## Portail

```bash
cd portal
cp .env.example .env      # VITE_API_BASE_URL pointe vers l'API
npm install
npm run dev
```

Portail sur <http://localhost:5173>.

## Tout via Docker

```bash
docker compose up --build
```

- Portail : <http://localhost:3000> (nginx sert le portail et proxifie `/api` + `/admin`)
- API : <http://localhost:8000>

## Base de données (optionnelle en dev)

```bash
docker compose up -d db
```

La base n'est requise que par les features qui persistent des données. La configuration
d'une base pour une instance réelle est gérée par l'[assistant de mise en place](installeur.md)
et détaillée dans [Langues & base de données](../administration/configuration.md).
