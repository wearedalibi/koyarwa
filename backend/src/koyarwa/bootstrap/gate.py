from __future__ import annotations

from collections.abc import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from koyarwa.core.instance import is_installed

# Chemins accessibles même en mode installation (l'assistant et ses ressources).
_EXEMPT_PREFIXES = ("/setup", "/admin/static")


class SetupGateMiddleware(BaseHTTPMiddleware):
    """Aiguillage selon l'état d'installation de l'instance.

    - Tant qu'elle n'est **pas installée** : tout est redirigé vers `/setup`
      (sauf l'assistant lui-même et ses ressources statiques).
    - Une fois **installée** : `/setup` est fermé et redirige vers `/admin`.
    """

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        path = request.url.path
        if not is_installed():
            if path.startswith(_EXEMPT_PREFIXES):
                return await call_next(request)
            return RedirectResponse("/setup", status_code=307)
        if path == "/setup" or path.startswith("/setup/"):
            return RedirectResponse("/admin", status_code=307)
        return await call_next(request)
