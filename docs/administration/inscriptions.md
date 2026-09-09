# Inscriptions

!!! info "Statut : 🔜 planifié"
    Modèle conçu, implémentation à venir (voir la [feuille de route](../feuille-de-route.md)).

L'**inscription** relie un utilisateur à un cours, en lui attribuant un rôle (le plus
souvent *étudiant*), une **méthode** et une **période** de validité.

## Méthodes d'inscription

Chaque cours active une ou plusieurs méthodes, selon ce que l'administrateur autorise :

| Méthode | Fonctionnement |
|---|---|
| **Manuelle** | l'enseignant inscrit et désinscrit les participants |
| **Auto-inscription** | l'apprenant s'inscrit lui-même, éventuellement avec une **clé d'inscription** |
| **Par cohorte** | tous les membres d'une cohorte sont inscrits d'un bloc |

Une méthode possède ses propres réglages : rôle attribué par défaut, clé éventuelle,
nombre maximal d'inscrits, période d'ouverture.

## Clé d'inscription

Mot de passe d'accès à un cours en auto-inscription. L'enseignant la communique à sa
classe ; l'apprenant la saisit une fois pour rejoindre le cours.

## Groupes et cohortes

- Un **groupe** organise les participants **à l'intérieur d'un cours** (ex. TP A / TP B).
  Utile pour séparer les rendus ou restreindre l'accès à certains contenus.
- Une **cohorte** est un ensemble d'utilisateurs **à l'échelle de l'établissement**
  (ex. « Promotion 2026 »). Elle permet d'inscrire tout un groupe de personnes à un cours
  en une opération.

## Cycle de vie

Une inscription peut être **active** ou **suspendue**, et bornée par des dates de début et
de fin — au-delà, l'accès au cours n'est plus effectif sans supprimer l'historique.
