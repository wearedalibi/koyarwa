"""Vérifications de sécurité au démarrage.

Empêche une instance **installée en production** de tourner avec des secrets
d'usine. Hors de ce cas (dev, ou avant installation), on se contente d'avertir —
la clé de session est de toute façon régénérée à l'installation.
"""

from __future__ import annotations

import logging

from koyarwa.core.config import settings
from koyarwa.core.instance import is_installed, resolve_session_secret

#: Valeur d'usine de la clé de session (cf. AdminSettings.session_secret).
_FACTORY_SESSION_SECRET = "dev-insecure-change-me"

_log = logging.getLogger("koyarwa.security")


def check_startup_security() -> None:
    """Échoue en prod installée si la clé de session est la valeur d'usine ; avertit sinon."""
    effective = resolve_session_secret(settings.admin.session_secret.get_secret_value())
    if effective == _FACTORY_SESSION_SECRET:
        detail = (
            "la clé de signature des sessions est encore la valeur d'usine "
            "(« dev-insecure-change-me »). Elle est normalement générée à "
            "l'installation ; sinon, définissez ADMIN_SESSION_SECRET."
        )
        if settings.app.is_prod and is_installed():
            raise RuntimeError(f"Configuration non sécurisée : {detail}")
        _log.warning("Sécurité : %s", detail)
