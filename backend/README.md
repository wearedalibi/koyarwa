# Koyarwa — Backend

FastAPI, architecture en tranches verticales (vertical slice).

## Prérequis
- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- (optionnel) Postgres — via `docker compose up -d db` à la racine

## Installation

```bash
cp .env.example .env      # ajuster si besoin
uv sync
uv run uvicorn koyarwa.main:app --reload
```

- API : http://localhost:8000
- Docs OpenAPI : http://localhost:8000/docs
- Health : `GET /api/v1/health`

> L'endpoint `health` ne dépend pas de la base : l'API démarre sans Postgres.
> La base n'est requise que par les features qui déclarent des modèles.

## Qualité

```bash
uv run ruff check .                       # lint
uv run ruff format .                      # format
uv run pytest                             # tests
uv run python scripts/dump_openapi.py     # régénère backend/openapi.json
```

## Arborescence

```
src/koyarwa/
├── main.py            # app FastAPI : CORS + rate limiting + montage du router
├── api/
│   ├── ratelimit.py   # middleware de limitation de débit (fenêtre glissante par IP)
│   └── v1/router.py   # agrégateur : inclut les routers des features
├── core/              # fondations transverses (aucun métier)
│   ├── config/        # settings par domaine (app, database, cors, ratelimit)
│   ├── env/           # résolution + cache du fichier .env
│   └── db/            # infra connexion : Base (DeclarativeBase) + session async
└── features/          # vertical slices (métier regroupé par feature)
    └── health/        # router de disponibilité
```

> **Organisation** : `core/` = fondations transverses (config, connexion DB),
> `features/` = métier en tranches verticales. Chaque feature possède son propre
> router, ses schémas, ses modèles et ses services. La règle de dépendance est
> unidirectionnelle : `features → core` (jamais l'inverse, ni feature → feature).

### Configuration

Tout passe par l'environnement, sans valeur en dur. Chaque section a son préfixe :
`APP_`, `DB_`, `CORS_`, `RATELIMIT_` (voir `.env.example`). L'accès se fait via
`settings.<section>.<champ>` (ex. `settings.db.url`, `settings.app.name`). Les
secrets sont des `SecretStr` et l'URL Postgres est composée à partir de ses composants.

### Ajouter une feature

1. Créer `features/<nom>/` avec, selon le besoin :
   - `router.py` — les endpoints (`APIRouter(prefix="/<nom>", tags=["<nom>"])`)
   - `schemas.py` — les DTO Pydantic (entrée/sortie)
   - `models.py` — les modèles SQLAlchemy (héritent de `core.db.Base`)
   - `service.py` — la logique métier
   - `ports.py` — les abstractions (Protocol) quand une dépendance doit être inversée
2. Inclure le router dans `api/v1/router.py`.
3. Si la feature a des modèles, les importer dans `scripts/init_db.py`.
4. Régénérer le contrat : `uv run python scripts/dump_openapi.py`.

## Notes production
- Ajouter Alembic pour le versionnage de schéma (à la place de `init_db.py`).
- Remplacer le rate limiter en mémoire par un store partagé (Redis) si l'API est répliquée.
