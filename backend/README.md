# Koyarwa — Backend

FastAPI, architecture en tranches verticales (vertical slice). **Deux canaux de
livraison au-dessus des mêmes services** : une **API JSON** (`/api/v1`, qui
alimente le portal) et un **back-office admin** HTML (`/admin`, Jinja + HTMX).

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

- API : http://localhost:8000  ·  docs : http://localhost:8000/docs
- Health : `GET /api/v1/health`
- Admin : http://localhost:8000/admin  (login : `ADMIN_USERNAME` / `ADMIN_PASSWORD`, défaut `admin` / `admin`)

> L'endpoint `health` et la feature d'exemple (dépôt en mémoire) ne dépendent pas
> de la base : l'API démarre sans Postgres. La base n'est requise que par les
> features qui déclarent des modèles.

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
├── main.py            # app FastAPI : sessions + CORS + rate limiting + routers (API & admin)
├── admin/             # back-office server-rendered (Jinja + HTMX)
│   ├── auth.py        # auth par session (cookie signé) + garde `require_admin`
│   ├── router.py      # pages HTML (login, annonces) + partiels HTMX
│   ├── templates/     # gabarits Jinja
│   └── static/        # htmx.min.js (vendu)
├── api/
│   ├── ratelimit.py   # middleware de limitation de débit (fenêtre glissante par IP)
│   └── v1/router.py   # agrégateur : inclut les routers d'API des features
├── core/              # fondations transverses (aucun métier)
│   ├── config/        # settings par domaine (app, admin, database, cors, ratelimit)
│   ├── env/           # résolution + cache du fichier .env
│   └── db/            # infra connexion : Base (DeclarativeBase) + session async
└── features/          # vertical slices (métier regroupé par feature)
    ├── health/        # router de disponibilité
    └── announcements/ # exemple : schemas · repository · service · router (API JSON)
```

> **Organisation** : `core/` = fondations transverses (config, connexion DB),
> `features/` = métier en tranches verticales. `api/` et `admin/` sont deux
> **adaptateurs** (JSON / HTML) au-dessus des mêmes `services`. Règle de dépendance
> unidirectionnelle : `adaptateurs → features → core`.

### Configuration

Tout passe par l'environnement, sans valeur en dur. Chaque section a son préfixe :
`APP_`, `ADMIN_`, `DB_`, `CORS_`, `RATELIMIT_` (voir `.env.example`). L'accès se fait via
`settings.<section>.<champ>` (ex. `settings.db.url`, `settings.admin.username`). Les
secrets sont des `SecretStr`.

### Back-office admin

Le module `admin/` est un **canal HTML** (Jinja + HTMX) parallèle à l'API JSON :
les deux consomment les mêmes **services** de `features/`. Auth par **session**
(cookie signé, préfixe `ADMIN_`), servi sous `/admin` (hors schéma OpenAPI).

Exemple livré : `/admin/announcements` (liste + création via HTMX) branché sur
`AnnouncementService` — dont l'API `GET`/`POST /api/v1/announcements` alimente le
portal. Le dépôt est **en mémoire** ; le remplacer par une implémentation
SQLAlchemy (même port `AnnouncementRepository`) suffit à persister, sans toucher
aux services ni aux routers.

> **Production** : remplacer le compte admin unique (`ADMIN_*`) par de vrais
> comptes en base + mots de passe hachés, et surcharger `ADMIN_SESSION_SECRET`.

### Ajouter une feature

1. Créer `features/<nom>/` avec, selon le besoin :
   - `schemas.py` — DTO Pydantic ·  `repository.py` — port + implémentation ·
     `service.py` — logique métier ·  `router.py` — endpoints API
2. Inclure le router d'API dans `api/v1/router.py` (et/ou exposer des pages dans `admin/`).
3. Si la feature a des modèles SQLAlchemy, créer une **migration Alembic** et les importer dans `migrations/env.py`.
4. Régénérer le contrat : `uv run python scripts/dump_openapi.py`.

## Notes production
- Le schéma est versionné par **Alembic** (`migrations/`) : `uv run alembic revision -m "…"` puis `uv run alembic upgrade head`.
- Remplacer le rate limiter en mémoire par un store partagé (Redis) si l'API est répliquée.
- Comptes admin en base + mots de passe hachés ; `ADMIN_SESSION_SECRET` fort.
