"""Traduction des libellés d'interface (français, anglais, allemand).

Catalogues JSON par langue (`locales/<lang>.json`). `translate(key, locale)` renvoie
la chaîne traduite, avec repli sur la langue par défaut puis sur la clé elle-même.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

DEFAULT_LANGUAGE = "fr"
SUPPORTED_LANGUAGES: tuple[str, ...] = ("fr", "en", "de")

_LOCALES_DIR = Path(__file__).resolve().parent / "locales"


@lru_cache(maxsize=len(SUPPORTED_LANGUAGES))
def _catalog(locale: str) -> dict[str, str]:
    path = _LOCALES_DIR / f"{locale}.json"
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_locale(locale: str | None) -> str:
    """Ramène une langue quelconque (`en-US`, `de_DE`…) à une langue supportée."""
    if not locale:
        return DEFAULT_LANGUAGE
    base = locale.replace("_", "-").split("-", 1)[0].lower()
    return base if base in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE


def translate(key: str, locale: str | None = None, /, **params: object) -> str:
    """Traduit `key` dans `locale` (replis : langue par défaut, puis la clé brute)."""
    lang = normalize_locale(locale)
    value = _catalog(lang).get(key)
    if value is None and lang != DEFAULT_LANGUAGE:
        value = _catalog(DEFAULT_LANGUAGE).get(key)
    if value is None:
        value = key
    return value.format(**params) if params else value
