from __future__ import annotations

import hmac

from starlette.requests import Request
from starlette.responses import RedirectResponse

from koyarwa.core.config import settings

#: Clé sous laquelle l'utilisateur admin est stocké dans la session.
SESSION_KEY = "admin_user"


class RequiresLogin(Exception):
    """Levée quand une page admin protégée est demandée sans session valide."""


def require_admin(request: Request) -> str:
    """Dépendance FastAPI : renvoie l'utilisateur en session, sinon exige un login."""
    user = request.session.get(SESSION_KEY)
    if not user:
        raise RequiresLogin
    return user


def verify_credentials(username: str, password: str) -> bool:
    """Compare aux identifiants configurés, en temps constant (anti timing-attack)."""
    ok_user = hmac.compare_digest(username, settings.admin.username)
    ok_password = hmac.compare_digest(password, settings.admin.password.get_secret_value())
    return ok_user and ok_password


async def requires_login_handler(request: Request, exc: RequiresLogin) -> RedirectResponse:
    """Handler d'exception : redirige les accès non authentifiés vers le login."""
    return RedirectResponse("/admin/login", status_code=303)
