# Vue d'ensemble

## Qu'est-ce que Koyarwa ?

Koyarwa est une **plateforme d'apprentissage en ligne** (LMS). Elle fournit à un
établissement un espace numérique où :

- des **enseignants** créent des cours, y déposent des ressources et des activités,
  inscrivent des apprenants, évaluent et suivent la progression ;
- des **apprenants** accèdent aux cours, rendent des devoirs, passent des tests et
  consultent leurs résultats ;
- des **administrateurs** configurent l'établissement, gèrent les comptes, les rôles,
  les catégories de cours et les réglages de l'instance.

## Une instance par établissement

Chaque établissement exploite **sa propre instance** de Koyarwa : un déploiement dédié,
avec sa **propre base de données**. Il n'y a pas de mélange de données entre
établissements — l'isolation est **physique**, pas seulement logique.

Concrètement :

- une instance = un établissement = une base de données ;
- la base peut être **PostgreSQL** ou **MySQL** (choisie à l'installation) ;
- la mise en place d'une instance passe par un [assistant d'installation](../demarrage/installeur.md)
  (langue, base de données, compte administrateur).

## Trois surfaces, un seul cœur

Koyarwa expose trois surfaces bâties sur une **couche de services** commune :

| Surface | Pour qui | Technologie |
|---|---|---|
| **Portail** | apprenants & enseignants | application React (SPA) |
| **Espace d'administration** | administrateurs | pages serveur (HTML + interactions légères) |
| **API REST** | le portail, les clients mobiles/tiers | JSON, versionnée (`/api/v1`) |

Le portail et l'espace d'administration ne dupliquent aucune logique métier : ils
consomment les **mêmes services**. Voir [Architecture](architecture.md).

## Capacités

!!! note "Statuts"
    ✅ disponible · 🔜 planifié (voir la [feuille de route](../feuille-de-route.md)).

- ✅ Socle d'API, espace d'administration, portail, conteneurisation.
- 🔜 Assistant de mise en place (langue, base de données, compte administrateur).
- 🔜 Internationalisation **français / anglais / allemand**.
- 🔜 Comptes, authentification, **rôles et permissions**.
- 🔜 Catégories, **cours** et sections.
- 🔜 **Inscriptions** (manuelle, auto-inscription par clé, cohortes).
- 🔜 **Activités et ressources** (devoir, test, forum, fichier…).
- 🔜 **Carnet de notes** et **suivi d'achèvement**.

## Pour qui est cette plateforme ?

Écoles primaires et secondaires, universités, centres de formation professionnelle,
organismes de formation continue — toute structure qui dispense des cours et doit en
suivre les résultats, pour un public francophone, anglophone ou germanophone.
