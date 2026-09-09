# Utilisateurs & rôles

!!! info "Statut : 🔜 planifié"
    Modèle conçu, implémentation à venir (voir la [feuille de route](../feuille-de-route.md)).

## Utilisateurs

Un **utilisateur** représente une personne : identifiant, e-mail, nom, préférences
(dont la **langue** d'interface) et état (actif/suspendu).

### Authentification

- **Local** — identifiant + mot de passe (haché). Disponible dès la première phase.
- **Auto-inscription** — un visiteur crée son compte lui-même (si l'administrateur l'autorise).
- **Import en masse** — création de comptes par fichier (CSV). 🔜
- **Fournisseurs externes** — OAuth, LDAP/annuaire. 🔜

Le premier compte (super-administrateur) est créé à l'[installation](../demarrage/installeur.md).

## Rôles et permissions

Les droits reposent sur trois notions : **rôle**, **capacité**, **portée**.

### Rôles standards

| Rôle | Peut… |
|---|---|
| **Super-administrateur** | tout, sur l'ensemble de l'instance |
| **Créateur de cours** | créer des cours (et y devenir enseignant) |
| **Enseignant** | gérer un cours : contenus, inscrits, évaluations |
| **Tuteur** *(enseignant non éditeur)* | évaluer, mais pas modifier le cours |
| **Étudiant** | accéder au cours et participer |
| **Invité** | consulter, en lecture seule, si autorisé |

### Capacités

Une **capacité** est une autorisation élémentaire, nommée par convention
`domaine.action` — par exemple :

- `course.manage` — modifier un cours
- `activity.grade` — évaluer une activité
- `enrol.manage` — gérer les inscriptions d'un cours
- `user.manage` — gérer les comptes

Un rôle est un **ensemble de capacités**. Chaque capacité peut être **autorisée**
(`allow`) ou **refusée** (`prevent`) pour un rôle.

### Portées

Un rôle est attribué à un utilisateur dans une **portée** :

```
Site  ⊃  Catégorie  ⊃  Cours
```

- Portée **site** : s'applique partout (ex. super-administrateur).
- Portée **catégorie** : s'applique à la catégorie et à ses cours.
- Portée **cours** : s'applique à un seul cours.

Les droits d'un utilisateur pour une action donnée se **résolvent du plus précis au plus
large** : cours → catégorie → site. On peut ainsi être *étudiant* dans un cours et
*enseignant* dans un autre.

!!! note "Simplicité assumée"
    La première version implémente rôles + capacités à ces trois portées, avec
    `allow`/`prevent`. Les redéfinitions fines par contexte pourront venir plus tard si
    le besoin apparaît.
