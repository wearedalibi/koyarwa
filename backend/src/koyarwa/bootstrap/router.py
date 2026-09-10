import logging
from pathlib import Path
from typing import Annotated
from zoneinfo import available_timezones

from fastapi import APIRouter, Form, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ValidationError

from koyarwa.bootstrap import service
from koyarwa.core.i18n import SUPPORTED_LANGUAGES, normalize_locale, translate
from koyarwa.core.instance import DatabaseConfig
from koyarwa.core.security import register_csrf
from koyarwa.core.security.passwords import hash_password
from koyarwa.features.identity.schemas import UserCreate
from koyarwa.features.site.schemas import SiteCreate

_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(_DIR / "templates"))
register_csrf(templates)

router = APIRouter(prefix="/setup", tags=["setup"], include_in_schema=False)

_SESSION_KEY = "setup"


class DatabaseForm(BaseModel):
    engine: str = "postgresql"
    host: str = "localhost"
    port: str = ""
    user: str = "koyarwa"
    password: str = ""
    name: str = "koyarwa"


class AdminForm(BaseModel):
    first_name: str = ""
    last_name: str = ""
    email: str
    username: str
    password: str
    email_visibility: str = "hidden"
    city: str = ""
    country: str = ""
    timezone: str = "UTC"
    description: str = ""


class SiteForm(BaseModel):
    full_name: str = ""
    short_name: str = ""
    description: str = ""
    timezone: str = "UTC"
    auth_method: str = "manual"
    noreply_email: str = ""
    support_email: str = ""


def _state(request: Request) -> dict:
    return dict(request.session.get(_SESSION_KEY, {}))


def _save_state(request: Request, state: dict) -> None:
    request.session[_SESSION_KEY] = state


_STEP_ORDER = ("language", "database", "admin", "site")

#: Options d'authentification proposées à l'installation.
_AUTH_METHODS = ("manual", "email")


def _context(request: Request, step: str, **extra: object) -> dict:
    lang = normalize_locale(_state(request).get("language"))

    def _t(key: str) -> str:
        return translate(key, lang)

    current = _STEP_ORDER.index(step) if step in _STEP_ORDER else 0
    steps = [
        {
            "n": i + 1,
            "label": _t(f"setup.step.{key}"),
            "state": "done" if i < current else "current" if i == current else "upcoming",
        }
        for i, key in enumerate(_STEP_ORDER)
    ]
    return {
        "step": step,
        "lang": lang,
        "languages": SUPPORTED_LANGUAGES,
        "t": _t,
        "steps": steps,
        **extra,
    }


def _first_error(exc: ValidationError) -> str:
    """Message de la première erreur de validation (pour l'installateur)."""
    errors = exc.errors()
    return str(errors[0].get("msg", "Données invalides.")) if errors else "Données invalides."


def _db_config(form: DatabaseForm) -> DatabaseConfig:
    return DatabaseConfig(
        engine=form.engine,
        host=form.host,
        port=int(form.port) if form.port.strip() else None,
        user=form.user,
        password=form.password,
        name=form.name,
    )


# ── Étape 1 : langue ────────────────────────────────────────────────
@router.get("", response_class=HTMLResponse)
def step_language(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "language.html", _context(request, "language"))


@router.post("")
def submit_language(request: Request, language: Annotated[str, Form()]) -> Response:
    _save_state(request, {**_state(request), "language": normalize_locale(language)})
    return RedirectResponse("/setup/database", status_code=303)


# ── Étape 2 : base de données ───────────────────────────────────────
@router.get("/database", response_class=HTMLResponse)
def step_database(request: Request) -> Response:
    form = _state(request).get("database", DatabaseForm().model_dump())
    return templates.TemplateResponse(
        request, "database.html", _context(request, "database", form=form)
    )


@router.post("/database/test", response_class=HTMLResponse)
async def test_database(request: Request, data: Annotated[DatabaseForm, Form()]) -> Response:
    ok, error = await service.test_connection(_db_config(data))
    lang = normalize_locale(_state(request).get("language"))
    return templates.TemplateResponse(
        request, "_db_test.html", {"ok": ok, "error": error, "t": lambda key: translate(key, lang)}
    )


@router.post("/database")
async def submit_database(request: Request, data: Annotated[DatabaseForm, Form()]) -> Response:
    ok, error = await service.test_connection(_db_config(data))
    if not ok:
        return templates.TemplateResponse(
            request,
            "database.html",
            _context(request, "database", form=data.model_dump(), error=error),
            status_code=400,
        )
    _save_state(request, {**_state(request), "database": data.model_dump()})
    return RedirectResponse("/setup/admin", status_code=303)


# ── Étape 3 : administrateur + finalisation ─────────────────────────
@router.get("/admin", response_class=HTMLResponse)
def step_admin(request: Request) -> Response:
    if "database" not in _state(request):
        return RedirectResponse("/setup/database", status_code=303)
    return templates.TemplateResponse(
        request, "admin.html", _context(request, "admin", timezones=sorted(available_timezones()))
    )


@router.post("/admin")
async def submit_admin(request: Request, data: Annotated[AdminForm, Form()]) -> Response:
    state = _state(request)
    if "database" not in state:
        return RedirectResponse("/setup/database", status_code=303)

    language = normalize_locale(state.get("language"))
    try:
        # Valide le compte (politique de mot de passe, e-mail, visibilité…).
        admin = UserCreate(
            username=data.username,
            email=data.email,
            password=data.password,
            first_name=data.first_name,
            last_name=data.last_name,
            email_visibility=data.email_visibility,
            city=data.city,
            country=data.country,
            timezone=data.timezone,
            description=data.description,
            lang=language,
        )
    except ValidationError as exc:
        return templates.TemplateResponse(
            request,
            "admin.html",
            _context(
                request, "admin", error=_first_error(exc), timezones=sorted(available_timezones())
            ),
            status_code=400,
        )

    # Le mot de passe est haché ICI : seul le hash transite en session, jamais le clair.
    draft = admin.model_dump(exclude={"password"})
    draft["password_hash"] = hash_password(admin.password)
    _save_state(request, {**state, "admin": draft})
    return RedirectResponse("/setup/site", status_code=303)


# ── Étape 4 : site + finalisation ───────────────────────────────────
@router.get("/site", response_class=HTMLResponse)
def step_site(request: Request) -> Response:
    if "admin" not in _state(request):
        return RedirectResponse("/setup/admin", status_code=303)
    return templates.TemplateResponse(
        request,
        "site.html",
        _context(
            request, "site", timezones=sorted(available_timezones()), auth_methods=_AUTH_METHODS
        ),
    )


@router.post("/site")
async def submit_site(request: Request, data: Annotated[SiteForm, Form()]) -> Response:
    state = _state(request)
    admin = state.get("admin")
    db_data = state.get("database")
    if not admin or not db_data:
        return RedirectResponse("/setup/admin", status_code=303)

    language = normalize_locale(state.get("language"))
    database = _db_config(DatabaseForm(**db_data))
    timezones = sorted(available_timezones())

    def _site_error(message: str, status: int) -> Response:
        return templates.TemplateResponse(
            request,
            "site.html",
            _context(
                request, "site", error=message, timezones=timezones, auth_methods=_AUTH_METHODS
            ),
            status_code=status,
        )

    try:
        site = SiteCreate(
            full_name=data.full_name,
            short_name=data.short_name,
            description=data.description,
            timezone=data.timezone,
            auth_method=data.auth_method,
            noreply_email=data.noreply_email,
            support_email=data.support_email,
        )
    except ValidationError as exc:
        return _site_error(_first_error(exc), 400)

    try:
        await service.finalize_install(
            language=language, database=database, admin=admin, site=site
        )
    except service.InstanceAlreadyInstalledError:
        return _site_error(translate("setup.error.already_installed", language), 409)
    except Exception:
        # Le détail (erreurs base/driver, DSN…) reste dans les journaux serveur ;
        # l'installateur ne reçoit qu'un message générique (pas de fuite d'info).
        logging.getLogger("koyarwa.setup").exception("Échec de la finalisation de l'installation")
        return _site_error(translate("setup.error.generic", language), 500)

    request.session.pop(_SESSION_KEY, None)
    return RedirectResponse("/admin", status_code=303)
