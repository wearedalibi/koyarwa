from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Form, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from koyarwa.bootstrap import service
from koyarwa.core.i18n import SUPPORTED_LANGUAGES, normalize_locale, translate
from koyarwa.core.instance import DatabaseConfig
from koyarwa.core.security import register_csrf
from koyarwa.features.identity.schemas import UserCreate

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
    name: str = ""
    email: str
    username: str
    password: str


def _state(request: Request) -> dict:
    return dict(request.session.get(_SESSION_KEY, {}))


def _save_state(request: Request, state: dict) -> None:
    request.session[_SESSION_KEY] = state


_STEP_ORDER = ("language", "database", "admin")


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
    return templates.TemplateResponse(request, "admin.html", _context(request, "admin"))


@router.post("/admin")
async def finalize(request: Request, data: Annotated[AdminForm, Form()]) -> Response:
    state = _state(request)
    db_data = state.get("database")
    if not db_data:
        return RedirectResponse("/setup/database", status_code=303)

    language = normalize_locale(state.get("language"))
    database = _db_config(DatabaseForm(**db_data))
    first_name, _, last_name = data.name.partition(" ")
    try:
        admin = UserCreate(
            username=data.username,
            email=data.email,
            password=data.password,
            first_name=first_name,
            last_name=last_name,
            lang=language,
        )
        await service.finalize_install(language=language, database=database, admin=admin)
    except Exception as exc:  # l'échec est rapporté à l'installateur
        return templates.TemplateResponse(
            request,
            "admin.html",
            _context(request, "admin", error=str(exc)),
            status_code=500,
        )

    request.session.pop(_SESSION_KEY, None)
    return RedirectResponse("/admin", status_code=303)
