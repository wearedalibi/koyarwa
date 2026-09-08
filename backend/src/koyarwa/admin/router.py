from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from koyarwa.admin.auth import SESSION_KEY, require_admin, verify_credentials
from koyarwa.features.announcements.ports import get_announcement_service
from koyarwa.features.announcements.schemas import AnnouncementCreate
from koyarwa.features.announcements.service import AnnouncementService

_ADMIN_DIR = Path(__file__).resolve().parent
#: Répertoire des fichiers statiques admin (monté par `main.py`).
ADMIN_STATIC_DIR = _ADMIN_DIR / "static"
templates = Jinja2Templates(directory=str(_ADMIN_DIR / "templates"))

router = APIRouter(prefix="/admin", tags=["admin"])

CurrentUser = Annotated[str, Depends(require_admin)]
ServiceDep = Annotated[AnnouncementService, Depends(get_announcement_service)]


@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "login.html", {"error": None})


@router.post("/login")
def login_submit(
    request: Request,
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
) -> Response:
    if verify_credentials(username, password):
        request.session[SESSION_KEY] = username
        return RedirectResponse("/admin/announcements", status_code=303)
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
