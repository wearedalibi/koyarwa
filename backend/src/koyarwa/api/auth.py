"""Authentification de l'API JSON (jeton de service Bearer).

Ferme l'écriture/lecture anonyme de l'API dès qu'un `API_TOKEN` est configuré.
Sans jeton configuré, l'API reste ouverte (confort de développement) et un
avertissement est émis au démarrage en production. L'authentification par
**utilisateur du portal** (jetons par compte) relève de la Phase 1 ; ce garde-fou
empêche entre-temps que l'API soit mondialement accessible en écriture.
"""

from __future__ import annotations

import hmac

from fastapi import HTTPException, status
from starlette.requests import Request

from koyarwa.core.config import settings


def require_api_token(request: Request) -> None:
    """Exige `Authorization: Bearer <API_TOKEN>` quand un jeton est configuré."""
    configured = settings.api.token.get_secret_value()
    if not configured:
        return  # API ouverte (dev) ; avertissement au démarrage en prod
    header = request.headers.get("authorization", "")
    scheme, _, token = header.partition(" ")
    if scheme.lower() != "bearer" or not hmac.compare_digest(token, configured):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Jeton d'API invalide ou absent.",
        )
