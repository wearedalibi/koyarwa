from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from koyarwa import __version__
from koyarwa.admin import ADMIN_STATIC_DIR, RequiresLogin, admin_router, requires_login_handler
from koyarwa.api.ratelimit import RateLimitMiddleware
from koyarwa.api.v1.router import api_router
from koyarwa.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Point d'extension pour le cycle de vie de l'app (démarrage / arrêt).

    Rien à initialiser pour l'instant. Y brancher plus tard ce qui doit vivre
    aussi longtemps que le process : pools, clients, tâches de fond, warmup...
    """
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app.name,
        version=__version__,
        debug=settings.app.debug,
        lifespan=lifespan,
    )

    # Sessions signées (cookie) — support de l'auth du back-office admin.
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.admin.session_secret.get_secret_value(),
        session_cookie=settings.admin.session_cookie,
        max_age=settings.admin.session_max_age,
        same_site="lax",
        https_only=settings.app.is_prod,
    )

    # Rate limiting ajouté avant CORS pour que CORS reste le middleware le plus
    # externe (les réponses 429 portent ainsi les en-têtes CORS). La santé est
    # exemptée pour ne pas gêner les sondes de disponibilité.
    if settings.ratelimit.enabled:
        app.add_middleware(
            RateLimitMiddleware,
            limit=settings.ratelimit.requests,
            window_seconds=settings.ratelimit.window_seconds,
            exempt_paths={f"{settings.app.api_v1_prefix}/health"},
        )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors.origins,
        allow_credentials=settings.cors.allow_credentials,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.app.api_v1_prefix)

    # Back-office admin (Jinja + HTMX) — hors schéma OpenAPI (canal HTML, pas l'API).
    app.mount("/admin/static", StaticFiles(directory=str(ADMIN_STATIC_DIR)), name="admin-static")
    app.include_router(admin_router, include_in_schema=False)
    app.add_exception_handler(RequiresLogin, requires_login_handler)

    return app


app = create_app()
