# Documentation Koyarwa

**Koyarwa** est une plateforme d'apprentissage en ligne (LMS, *Learning Management
System*) open source. Elle permet à un établissement — école, université, centre de
formation — de créer des **cours**, d'y inscrire des **apprenants**, d'y publier des
**activités** et **ressources**, puis de **suivre et d'évaluer** la progression.

Koyarwa se déploie **en instance par établissement** : chaque organisation dispose de
sa propre installation et de sa propre base de données, isolées des autres.

## Par où commencer ?

| Vous êtes… | Commencez par |
|---|---|
| **Curieux** de la plateforme | [Vue d'ensemble](introduction/vue-densemble.md) · [Concepts clés](introduction/concepts-cles.md) |
| **Administrateur** qui installe une instance | [Assistant de mise en place](demarrage/installeur.md) |
| **Administrateur** au quotidien | [Espace d'administration](administration/espace-administration.md) |
| **Enseignant** | [Cours, activités & notes](pedagogie/cours-activites-et-notes.md) |
| **Développeur / intégrateur** | [Architecture](introduction/architecture.md) · [API](api/reference-api.md) · [Développement](developpement/guide.md) |

## Organisation de cette documentation

- **Introduction** — ce qu'est Koyarwa, son vocabulaire, son architecture.
- **Démarrage** — installer l'environnement de développement, puis mettre en place une instance.
- **Administration** — gérer une instance : espace admin, utilisateurs, rôles, inscriptions, langues et base de données.
- **Pédagogie** — gérer un cours : sections, activités, ressources, notes, suivi.
- **Modèle de données** — les entités du domaine et les décisions structurantes.
- **API** — l'interface REST qui alimente le portail.
- **Développement** — structure du code et conventions pour contribuer.
- **Feuille de route** — ce qui est livré et ce qui vient.

## Statut du projet

Koyarwa est en construction. Chaque page indique le statut de ce qu'elle décrit :

!!! note "Légende des statuts"
    - ✅ **Disponible** — implémenté et testé.
    - 🔨 **En cours** — en cours d'implémentation.
    - 🔜 **Planifié** — conçu, pas encore implémenté (voir la [feuille de route](feuille-de-route.md)).

À ce jour, le **socle applicatif** (API, espace d'administration, portail) est en place ;
le **domaine pédagogique** (cours, activités, notes) et l'**assistant de mise en place**
sont conçus et planifiés. Reportez-vous à la [feuille de route](feuille-de-route.md) pour le détail par phase.
