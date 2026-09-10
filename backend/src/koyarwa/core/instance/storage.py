"""Écriture de fichiers d'instance à permissions restreintes.

Le dossier d'instance contient des secrets (identifiants de base, clé de session,
jeton d'installation). Ces fichiers doivent rester lisibles par le **seul
propriétaire** du process : dossier en ``0700``, fichiers en ``0600``.

Sur les systèmes sans permissions POSIX (montages Windows, certains volumes), le
``chmod`` est sans effet et simplement ignoré — la protection repose alors sur
l'isolation du volume.
"""

from __future__ import annotations

import os
from pathlib import Path

_DIR_MODE = 0o700
_FILE_MODE = 0o600


def _chmod(path: Path, mode: int) -> None:
    """Resserre les permissions, en tolérant les systèmes de fichiers non POSIX."""
    try:
        os.chmod(path, mode)
    except OSError:
        pass


def ensure_private_dir(path: Path) -> None:
    """Crée le répertoire au besoin et restreint ses permissions (0700)."""
    path.mkdir(parents=True, exist_ok=True)
    _chmod(path, _DIR_MODE)


def write_private_text(path: Path, content: str) -> None:
    """Écrit un fichier UTF-8 lisible par le seul propriétaire (0600).

    La création se fait directement en ``0600`` (le ``umask`` ne peut pas élargir
    les bits propriétaire), puis un ``chmod`` resserre un fichier préexistant.
    """
    ensure_private_dir(path.parent)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, _FILE_MODE)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(content)
    _chmod(path, _FILE_MODE)
