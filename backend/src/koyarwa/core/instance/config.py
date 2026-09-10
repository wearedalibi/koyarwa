"""Configuration d'instance persistante.

Une instance installée écrit ici son moteur de base, ses identifiants de connexion et
sa langue, ainsi qu'un indicateur `installed` (le verrou d'installation). Ce fichier vit
**hors du dépôt** — dans le répertoire d'instance, monté sur volume en conteneur : il
contient des secrets et n'est jamais committé.

Le répertoire est résolu via `KOYARWA_INSTANCE_DIR` (sinon `./instance`).
"""

from __future__ import annotations

import os
import tomllib
from dataclasses import asdict, dataclass
from pathlib import Path

import tomli_w

from koyarwa.core.config.database import build_async_url
from koyarwa.core.instance.storage import write_private_text

INSTANCE_DIR_ENV = "KOYARWA_INSTANCE_DIR"
CONFIG_FILENAME = "config.toml"


def instance_dir() -> Path:
    """Répertoire d'instance : `KOYARWA_INSTANCE_DIR` sinon `./instance`."""
    override = os.environ.get(INSTANCE_DIR_ENV)
    return Path(override) if override else Path.cwd() / "instance"


def config_path() -> Path:
    return instance_dir() / CONFIG_FILENAME


@dataclass(frozen=True)
class DatabaseConfig:
    engine: str
    host: str
    user: str
    password: str
    name: str
    port: int | None = None


@dataclass(frozen=True)
class InstanceConfig:
    installed: bool
    language: str
    database: DatabaseConfig | None = None
    #: Clé de signature des cookies de session, générée aléatoirement à
    #: l'installation (façon salts WordPress). Absente tant que non installé.
    secret_key: str | None = None


def load() -> InstanceConfig | None:
    """Charge la config d'instance, ou `None` si l'instance n'est pas configurée."""
    path = config_path()
    if not path.is_file():
        return None
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    db = data.get("database")
    secret = data.get("secret_key")
    return InstanceConfig(
        installed=bool(data.get("installed", False)),
        language=str(data.get("language", "fr")),
        database=DatabaseConfig(**db) if db else None,
        secret_key=str(secret) if secret else None,
    )


def save(config: InstanceConfig) -> None:
    """Écrit la config d'instance à permissions restreintes (0600) — contient des secrets."""
    doc: dict[str, object] = {"installed": config.installed, "language": config.language}
    if config.secret_key:
        doc["secret_key"] = config.secret_key
    if config.database is not None:
        doc["database"] = {k: v for k, v in asdict(config.database).items() if v is not None}
    write_private_text(config_path(), tomli_w.dumps(doc))


def is_installed() -> bool:
    """L'instance est-elle installée (verrou posé) ?"""
    cfg = load()
    return bool(cfg and cfg.installed)


def resolve_session_secret(fallback: str) -> str:
    """Clé de signature des sessions : celle générée à l'installation, sinon `fallback`.

    Une fois l'instance installée, la clé aléatoire persistée l'emporte sur la
    valeur d'environnement/par défaut ; l'application doit être redémarrée pour la
    prendre en compte (le middleware de session est figé au démarrage).
    """
    cfg = load()
    if cfg and cfg.secret_key:
        return cfg.secret_key
    return fallback


def instance_language() -> str | None:
    cfg = load()
    return cfg.language if cfg else None


def database_url() -> str | None:
    """URL SQLAlchemy async d'après la config d'instance, ou `None` si absente.

    Indépendant du verrou `installed` : dès que la base est configurée (même en
    cours d'installation), l'application s'y connecte.
    """
    cfg = load()
    if not cfg or cfg.database is None:
        return None
    d = cfg.database
    return build_async_url(
        engine=d.engine, host=d.host, port=d.port, user=d.user, password=d.password, name=d.name
    )
