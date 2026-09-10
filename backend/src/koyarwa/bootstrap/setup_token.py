"""Jeton d'installation — protège l'assistant `/setup`.

Tant que l'instance n'est pas installée, un jeton aléatoire est généré et **affiché
dans les logs du serveur** au démarrage. L'assistant l'exige avant toute
configuration : seul qui a accès à la console/aux logs du serveur peut installer
(parade à la « course à l'installation »). Le jeton est oublié une fois installé.

Il est persisté dans le dossier d'instance si possible (partagé entre workers) ;
si le dossier n'est pas inscriptible (ex. Controlled Folder Access sous Windows),
on retombe sur une valeur en mémoire du process.
"""

from __future__ import annotations

import hmac
import secrets
from pathlib import Path

from koyarwa.core.instance import instance_dir

_TOKEN_FILENAME = "setup_token"
_cached: str | None = None


def _token_path() -> Path:
    return instance_dir() / _TOKEN_FILENAME


def get_or_create_token() -> str:
    """Renvoie le jeton courant (persisté si possible, sinon gardé en mémoire)."""
    global _cached
    path = _token_path()
    try:
        if path.is_file():
            existing = path.read_text(encoding="utf-8").strip()
            if existing:
                return existing
    except OSError:
        pass
    if _cached:
        return _cached
    token = secrets.token_urlsafe(24)
    _cached = token
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(token, encoding="utf-8")
    except OSError:
        pass  # dossier non inscriptible → le jeton reste en mémoire
    return token


def verify_token(candidate: str) -> bool:
    """Compare en temps constant au jeton courant."""
    return hmac.compare_digest(candidate.strip(), get_or_create_token())


def clear_token() -> None:
    """Oublie le jeton (à appeler une fois l'installation terminée)."""
    global _cached
    _cached = None
    try:
        _token_path().unlink(missing_ok=True)
    except OSError:
        pass
