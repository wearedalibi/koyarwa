import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from koyarwa import __version__
from koyarwa.admin import ADMIN_STATIC_DIR, RequiresLogin, admin_router, requires_login_handler
from koyarwa.api.ratelimit import RateLimitMiddleware
from koyarwa.api.v1.router import api_router
from koyarwa.bootstrap import SetupGateMiddleware, setup_router
from koyarwa.core.config import settings
from koyarwa.core.instance import is_installed, resolve_session_secret
from koyarwa.core.security import csrf_protect
from koyarwa.core.security.checks import check_startup_security


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Cycle de vie de l'app.

    Signale au démarrage qu'une instance non installée expose l'assistant `/setup`.
    """
    check_startup_security()
    if not is_installed():
        logging.getLogger("koyarwa.setup").warning(
            "Instance NON installée — ouvrez l'assistant de mise en place sur /setup."
        )
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app.name,
        version=__version__,
        debug=settings.app.debug,
        lifespan=lifespan,
    )

    # Sessions signées (cookie) — support de l'auth du back-office admin.
    # La clé générée à l'installation prime sur la valeur par défaut d'usine ;
    # à défaut (avant installation), on retombe sur celle de l'environnement.
    app.add_middleware(
        SessionMiddleware,
        secret_key=resolve_session_secret(settings.admin.session_secret.get_secret_value()),
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
            trust_proxy=settings.ratelimit.trust_proxy,
        )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors.origins,
        allow_credentials=settings.cors.allow_credentials,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Setup-gate (le middleware le plus externe) : tant que l'instance n'est pas
    # installée, tout est redirigé vers l'assistant `/setup` ; une fois installée,
    # `/setup` est fermé.
    app.add_middleware(SetupGateMiddleware)

    app.include_router(api_router, prefix=settings.app.api_v1_prefix)

    # Back-office admin (Jinja + HTMX) — hors schéma OpenAPI (canal HTML, pas l'API).
    # Les formulaires HTML (admin + assistant) sont protégés contre le CSRF ; l'API
    # JSON du portal, authentifiée par jeton et non par cookie, en est dispensée.
    app.mount("/admin/static", StaticFiles(directory=str(ADMIN_STATIC_DIR)), name="admin-static")
    app.include_router(admin_router, include_in_schema=False, dependencies=[Depends(csrf_protect)])
    app.include_router(setup_router, dependencies=[Depends(csrf_protect)])

    app.add_exception_handler(RequiresLogin, requires_login_handler)

    return app


app = create_app()
