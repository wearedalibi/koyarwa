# Espace d'administration

L'**espace d'administration** (`/admin`) réunit les écrans de gestion réservés aux
administrateurs. Il est rendu **côté serveur** (pages HTML avec interactions légères),
distinct du [portail](../introduction/vue-densemble.md#trois-surfaces-un-seul-coeur)
destiné aux apprenants et enseignants.

!!! info "Statut"
    ✅ Espace d'administration, connexion par session, page d'exemple *Annonces*.
    🔜 Écrans de gestion des utilisateurs, rôles, cours, inscriptions.

## Accès et connexion

- URL : `/admin` (ex. <http://localhost:8000/admin>).
- Authentification par **session** (cookie signé). Une page protégée demandée sans
  session valide redirige vers `/admin/login`.
- Les identifiants du premier administrateur sont créés à l'[installation](../demarrage/installeur.md).

!!! warning "Compte administrateur en développement"
    Tant que l'authentification en base n'est pas livrée, l'espace d'administration
    utilise un **compte unique** défini par la configuration (`ADMIN_USERNAME`,
    `ADMIN_PASSWORD`). À remplacer par des comptes en base + mots de passe hachés
    (voir [Utilisateurs & rôles](utilisateurs-et-roles.md)).

## Ce que l'on y fait

L'espace d'administration couvrira la gestion de l'instance :

- **Utilisateurs** — comptes, authentification, réinitialisation ([détail](utilisateurs-et-roles.md)).
- **Rôles & permissions** — attribution des rôles par portée ([détail](utilisateurs-et-roles.md#roles-et-permissions)).
- **Catégories & cours** — organisation de l'offre de formation ([détail](../pedagogie/cours-activites-et-notes.md)).
- **Inscriptions** — méthodes d'inscription, cohortes ([détail](inscriptions.md)).
- **Langues & base de données** — réglages de l'instance ([détail](configuration.md)).

## Un service, deux canaux

L'espace d'administration et l'API **partagent la même couche de services**. Une donnée
créée depuis un écran d'administration est immédiatement disponible via l'API qui alimente
le portail, et inversement — sans logique dupliquée. C'est le motif appliqué dès la
feature d'exemple *Annonces* :

- Administration : `/admin/announcements` (liste + création).
- API : `GET`/`POST /api/v1/announcements` (consommée par le portail).

## Apparence

L'espace d'administration adopte un habillage cohérent (typographie, couleurs de marque,
icônes) et un **thème clair/sombre** automatique. Les composants (formulaires, tableaux,
boutons) suivent un jeu de *design tokens* défini au niveau de l'instance.
