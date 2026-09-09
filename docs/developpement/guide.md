# Développement

Conventions pour contribuer au backend. Prérequis et commandes : voir
[Installation (développement)](../demarrage/installation-developpement.md).

## Structure du code

```
backend/src/koyarwa/
├── main.py            # composition de l'app : middlewares + routeurs (API & admin)
├── api/v1/router.py   # agrège les routeurs d'API des features
├── admin/             # espace d'administration (pages serveur)
├── core/              # fondations transverses (config · env · db)
└── features/          # une tranche verticale par domaine
```

**Règle de dépendance** : `api` / `admin` → `features` → `core`. Jamais `feature → feature`
en direct : une feature expose des **services** que d'autres consomment via un port.

## Ajouter une feature

1. Créer `features/<nom>/` avec, selon le besoin :
     - `schemas.py` — DTO Pydantic (entrée/sortie) ;
     - `models.py` — tables SQLAlchemy (héritent de `core.db.Base`) ;
     - `repository.py` — **port** (Protocol) + implémentation ;
     - `service.py` — logique métier, indépendante du canal ;
     - `router.py` — endpoints d'API.
2. Inclure le routeur d'API dans `api/v1/router.py`.
3. Exposer, si besoin, des écrans dans `admin/`.
4. Ajouter une **migration** pour les nouvelles tables.
5. Régénérer le contrat : `uv run python scripts/dump_openapi.py`.
6. Écrire les tests correspondants.

## Principes

**Un service, deux canaux.** L'API et l'espace d'administration consomment les **mêmes
services**. Aucune règle métier ne vit dans un routeur.

**Le port repository isole la base.** Le service dépend d'une abstraction, pas d'un moteur.
C'est ce qui permet de viser PostgreSQL et MySQL avec une seule logique, et de tester
avec une implémentation en mémoire.

**Configuration par sections.** Aucune valeur métier en dur : tout via
`settings.<section>.<champ>` (préfixes `APP_`, `ADMIN_`, `DB_`, `CORS_`, `RATELIMIT_`).
Les secrets sont des `SecretStr`.

**Contrat d'API versionné.** `backend/openapi.json` est committé et vérifié par un test —
le portail en dérive. Régénérer après toute modification des schémas ou des endpoints.

## Qualité

```bash
uv run ruff check .     # lint
uv run ruff format .    # format
uv run pytest           # tests
```

Le style est aligné sur l'outil (ligne 100, cible py312). Les endpoints utilisent des
dépendances typées via `Annotated[...]`.

## Migrations 🔜

Le versionnage du schéma s'appuiera sur **Alembic** (à introduire en Phase 0, en
remplacement du script d'initialisation). Les migrations doivent rester compatibles avec
PostgreSQL **et** MySQL.

## Portail

Le portail (`portal/`) est une application **React + Fluent UI** (build Vite). Il consomme
l'API via un client configuré par `VITE_API_BASE_URL`. Les libellés d'interface passeront
par une bibliothèque d'internationalisation (fr/en/de).
