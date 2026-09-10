"""Protection CSRF des formulaires HTML (back-office admin + assistant d'installation).

Modèle du « jeton synchroniseur » : un jeton aléatoire est déposé dans la session
signée du visiteur, puis exigé — via un champ caché du formulaire **ou** l'en-tête
``X-CSRF-Token`` — sur toute requête mutante (POST/PUT/PATCH/DELETE). La comparaison
se fait en temps constant.

Les canaux JSON (API du portal) ne sont pas concernés : ils s'authentifient par
jeton et non par cookie de session, donc ne sont pas vulnérables au CSRF.
"""

from __future__ import annotations

import hmac
import secrets

from fastapi import HTTPException, status
from fastapi.templating import Jinja2Templates
from jinja2 import pass_context
from jinja2.runtime import Context
from markupsafe import Markup
from starlette.requests import Request

#: Clé du jeton dans la session, nom du champ de formulaire et de l'en-tête HTTP.
_SESSION_KEY = "csrf_token"
_FIELD_NAME = "csrf_token"
_HEADER_NAME = "x-csrf-token"

#: Méthodes sans effet de bord : dispensées de vérification.
_SAFE_METHODS = frozenset({"GET", "HEAD", "OPTIONS", "TRACE"})


def issue_csrf(request: Request) -> str:
    """Renvoie le jeton CSRF de la session, en le créant à la première demande."""
    token = request.session.get(_SESSION_KEY)
    if not token:
        token = secrets.token_urlsafe(32)
        request.session[_SESSION_KEY] = token
    return token


async def csrf_protect(request: Request) -> None:
    """Dépendance FastAPI : exige un jeton CSRF valide sur les requêtes mutantes.

    Les méthodes sûres passent sans contrôle. Le jeton soumis est cherché d'abord
    dans l'en-tête ``X-CSRF-Token`` (requêtes HTMX/fetch), sinon dans le champ
    caché ``csrf_token`` du formulaire.
    """
    if request.method in _SAFE_METHODS:
        return

    expected = request.session.get(_SESSION_KEY)
    submitted = request.headers.get(_HEADER_NAME)
    if not submitted:
        try:
            form = await request.form()
        except Exception:  # corps non-formulaire : aucun jeton exploitable
            form = None
        if form is not None:
            value = form.get(_FIELD_NAME)
            submitted = value if isinstance(value, str) else None

    if not (expected and submitted and hmac.compare_digest(submitted, expected)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Jeton CSRF invalide ou absent.",
        )


@pass_context
def _csrf_input(context: Context) -> Markup:
    """Champ caché à insérer dans chaque formulaire : ``{{ csrf_input() }}``."""
    request: Request = context["request"]
    token = issue_csrf(request)
    return Markup(f'<input type="hidden" name="{_FIELD_NAME}" value="{token}">')


def register_csrf(templates: Jinja2Templates) -> None:
    """Expose ``csrf_input()`` aux gabarits Jinja fournis."""
    templates.env.globals["csrf_input"] = _csrf_input
