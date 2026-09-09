# API

Le backend expose une **API REST** en JSON qui alimente le [portail](../introduction/vue-densemble.md)
et, à terme, des clients mobiles ou tiers.

!!! info "Statut"
    ✅ Socle d'API versionnée, contrat OpenAPI, endpoints `health` et `announcements`.
    🔜 Endpoints du domaine pédagogique (cours, inscriptions, activités, notes).

## Conventions

- **Versionnement** — toutes les routes sous `/api/v1`.
- **Format** — JSON en entrée et sortie ; corps validés par des schémas typés.
- **Documentation vivante** — schéma OpenAPI exposé sur `/docs` (interactif) et `/openapi.json`.
- **Contrat versionné** — `backend/openapi.json` est **committé** dans le dépôt et vérifié
  par un test : le portail dérive de ce contrat, ce qui empêche toute dérive silencieuse.

## Endpoints disponibles

| Méthode | Route | Description |
|---|---|---|
| `GET` | `/api/v1/health` | disponibilité du service (`status`, `version`) |
| `GET` | `/api/v1/announcements` | liste des annonces (exemple) |
| `POST` | `/api/v1/announcements` | crée une annonce (exemple) |

L'espace d'administration (`/admin`) n'appartient pas à l'API : c'est un canal HTML, exclu
du schéma OpenAPI.

## Authentification 🔜

- **Portail (première partie)** — session par cookie sécurisé, même origine que l'API.
- **Clients mobiles / tiers** — jetons (type *Bearer*).

## Sécurité

- **Limitation de débit** — fenêtre glissante par IP (l'endpoint de disponibilité est exempté).
- **CORS** — origines autorisées configurables (le portail en développement).
- **Messages d'erreur** — le détail interne (traces, chaînes de connexion) reste côté
  serveur ; le client reçoit un message générique.

## Exemple

```bash
curl http://localhost:8000/api/v1/health
# {"status":"ok","version":"0.1.0"}
```
