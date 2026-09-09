# Feuille de route

Koyarwa se construit par **cercles concentriques** : d'abord une plateforme installable et
utilisable, puis la profondeur pédagogique, puis l'écosystème.

!!! note "Statuts"
    ✅ disponible · 🔨 en cours · 🔜 planifié

## Déjà en place ✅

Le **socle applicatif** :

- API FastAPI (architecture en tranches verticales), limitation de débit, CORS.
- **Espace d'administration** (pages serveur) avec connexion par session, habillage et
  thème clair/sombre.
- **Portail** React + Fluent UI (consommation de l'API).
- Feature d'exemple **Annonces** (service + repository) exposée par l'API **et** l'administration.
- Contrat **OpenAPI** committé + tests ; conteneurisation Docker (backend + portail).

## Phase 0 — Mise en place 🔜

Rendre une instance **installable** par un établissement.

- **Assistant d'installation** : langue → base de données (test de connexion) → migrations
  → compte super-administrateur → verrouillage.
- **Internationalisation** français / anglais / allemand (interface).
- **Connexion à la base** paresseuse + configuration d'instance persistante.
- **PostgreSQL & MySQL** via l'abstraction unique ; **Alembic** pour les migrations.

## Phase 1 — LMS minimal utilisable 🔜

Le plus petit ensemble qui fait un vrai LMS.

- **Identité** : comptes, authentification locale (mots de passe hachés).
- **Rôles & permissions** : rôles + capacités à trois portées.
- **Catalogue** : catégories, cours, sections.
- **Inscriptions** : manuelle + auto-inscription par clé.
- **Activités** : ressource + devoir.
- **Notes** : élément de note + saisie.
- **Administration** (CRUD) et **API** correspondantes pour le portail.

## Phase 2 — Profondeur pédagogique 🔜

- **Test** + banque de questions ; **forum**.
- **Groupes & groupements** ; **cohortes**.
- **Achèvement** + conditions d'accès.
- **Carnet de notes** complet (catégories, agrégation, barèmes).
- Authentification externe (OAuth / annuaire) ; import CSV.

## Phase 3 — Écosystème 🔜

- **Badges** & compétences.
- **Atelier** (évaluation par les pairs).
- Standards d'interopérabilité (contenus & outils externes).
- **Messagerie** & notifications.
- Application **mobile**.
- Assistance par **IA**.

---

Le détail des entités par module est en
[Modèle de données](modele-de-donnees/reference-entites.md).
