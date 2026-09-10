from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from koyarwa.admin.auth import SESSION_KEY, login_throttle, require_admin
from koyarwa.core.security import register_csrf
from koyarwa.features.announcements.ports import get_announcement_service
from koyarwa.features.announcements.schemas import AnnouncementCreate
from koyarwa.features.announcements.service import AnnouncementService
from koyarwa.features.identity.ports import get_user_service
from koyarwa.features.identity.service import UserService

_ADMIN_DIR = Path(__file__).resolve().parent
#: Répertoire des fichiers statiques admin (monté par `main.py`).
ADMIN_STATIC_DIR = _ADMIN_DIR / "static"
templates = Jinja2Templates(directory=str(_ADMIN_DIR / "templates"))
register_csrf(templates)

router = APIRouter(prefix="/admin", tags=["admin"])

CurrentUser = Annotated[str, Depends(require_admin)]
ServiceDep = Annotated[AnnouncementService, Depends(get_announcement_service)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]


@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "login.html", {"error": None})


@router.post("/login")
async def login_submit(
    request: Request,
    service: UserServiceDep,
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
) -> Response:
    # Verrou anti-force-brute : refuse les tentatives d'un compte trop sollicité.
    if login_throttle.locked_for(username) > 0:
        return templates.TemplateResponse(
            request,
            "login.html",
            {"error": "Trop de tentatives échouées. Réessayez dans quelques minutes."},
            status_code=429,
        )
    # Authentification sur le super-administrateur en base (créé à l'installation).
    user = await service.authenticate(username, password)
    if user is not None and user.is_superuser:
        login_throttle.reset(username)
        request.session[SESSION_KEY] = user.username
        return RedirectResponse("/admin/announcements", status_code=303)
    login_throttle.record_failure(username)
    return templates.TemplateResponse(
        request, "login.html", {"error": "Identifiants invalides."}, status_code=401
    )


@router.get("/logout")
def logout(request: Request) -> RedirectResponse:
    request.session.clear()
    return RedirectResponse("/admin/login", status_code=303)


@router.get("")
def admin_home(user: CurrentUser) -> RedirectResponse:
    return RedirectResponse("/admin/announcements", status_code=303)


@router.get("/announcements", response_class=HTMLResponse)
def announcements_page(request: Request, user: CurrentUser, service: ServiceDep) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "announcements/list.html",
        {"user": user, "announcements": service.list()},
    )


@router.post("/announcements", response_class=HTMLResponse)
def announcements_create(
    request: Request,
    user: CurrentUser,
    service: ServiceDep,
    title: Annotated[str, Form()],
    body: Annotated[str, Form()],
) -> HTMLResponse:
    item = service.create(AnnouncementCreate(title=title, body=body))
    # Partiel HTMX : la nouvelle ligne, insérée en tête du tableau (#rows).
    return templates.TemplateResponse(request, "announcements/_row.html", {"a": item})
