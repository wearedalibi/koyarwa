"""En-têtes de sécurité HTTP (défense en profondeur) sur toutes les réponses.

La CSP est **pragmatique** : le back-office est rendu côté serveur avec des
scripts/styles en ligne et htmx (qui évalue les attributs `hx-on`), d'où
`'unsafe-inline'`/`'unsafe-eval'` pour les scripts. Le reste est verrouillé —
sources limitées à l'origine, cadrage interdit (anti-clickjacking), `object-src`
et `base-uri` fermés, `form-action` bornée. L'autoescape Jinja reste la première
défense anti-XSS ; la CSP pourra être durcie plus tard via des nonces.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

_CSP = "; ".join(
    (
        "default-src 'self'",
        "script-src 'self' 'unsafe-inline' 'unsafe-eval'",
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
        "font-src 'self' https://fonts.gstatic.com",
        "img-src 'self' data:",
        "connect-src 'self'",
        "object-src 'none'",
        "base-uri 'self'",
        "form-action 'self'",
        "frame-ancestors 'none'",
    )
)

_HSTS = "max-age=31536000; includeSubDomains"


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Pose les en-têtes de sécurité (HSTS uniquement quand `hsts=True`, càd en prod/TLS)."""

    def __init__(self, app: Callable, *, hsts: bool = False) -> None:
        super().__init__(app)
        self._hsts = hsts

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        response = await call_next(request)
        headers = response.headers
        headers.setdefault("Content-Security-Policy", _CSP)
        headers.setdefault("X-Content-Type-Options", "nosniff")
        headers.setdefault("X-Frame-Options", "DENY")
        headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        if self._hsts:
            headers.setdefault("Strict-Transport-Security", _HSTS)
        return response
