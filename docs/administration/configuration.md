# Langues & base de données

Réglages définis à la mise en place de l'instance, puis ajustables par l'administrateur.

## Langues (internationalisation)

!!! info "Statut : 🔜 planifié"

Koyarwa est prévu pour fonctionner en **français**, **anglais** et **allemand**.

- **Langue de l'instance** — langue par défaut, choisie à l'[installation](../demarrage/installeur.md).
- **Langue de l'utilisateur** — chaque compte peut choisir sa langue d'interface ; à défaut,
  celle de l'instance s'applique.
- **Sélecteur de langue** — présent dès l'assistant d'installation, puis dans l'interface.

Ce qui est traduit : les **libellés de l'interface** (portail et espace d'administration).
Les **contenus pédagogiques** (intitulés de cours, énoncés) sont saisis par les
enseignants dans la langue de leur choix et ne sont pas traduits automatiquement.

Techniquement, les traductions reposent sur des **catalogues de messages** (un par
langue) côté backend/administration, et sur des catalogues équivalents côté portail.

## Base de données

!!! info "Statut : 🔜 planifié (moteurs), ✅ socle SQLAlchemy en place"

Une instance utilise **une** base de données, choisie à l'installation :

| Moteur | Support |
|---|---|
| **PostgreSQL** | ✅ visé en premier |
| **MySQL** (MariaDB) | ✅ visé en premier |

Les deux moteurs sont adressés via une **couche d'abstraction unique** (SQLAlchemy) :
la logique métier ne connaît pas le dialecte. Les différences de dialecte (types JSON,
booléens…) sont absorbées à ce niveau.

!!! note "Pourquoi pas d'autres moteurs pour l'instant ?"
    Le domaine d'un LMS est fortement **relationnel** (inscriptions, notes, rôles,
    intégrité référentielle, transactions). Les moteurs relationnels sont donc le terrain
    naturel. L'architecture *repository* laisse la porte ouverte à d'autres backends
    ultérieurement, mais chacun a un coût réel ; ils ne sont pas au programme initial.

### Connexion

Les paramètres de connexion (moteur, hôte, port, utilisateur, mot de passe, base) sont
saisis dans l'[assistant de mise en place](../demarrage/installeur.md), **testés** avant
validation, puis écrits dans la configuration d'instance. L'URL de connexion est
**composée** à partir de ces champs ; le mot de passe est traité comme un secret.

### Schéma et migrations

Le schéma des tables est géré par des **migrations** versionnées, appliquées à
l'installation puis à chaque mise à jour. Les migrations sont écrites pour rester
compatibles avec les moteurs supportés.
