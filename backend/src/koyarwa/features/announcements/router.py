from typing import Annotated

from fastapi import APIRouter, Depends

from koyarwa.features.announcements.ports import get_announcement_service
from koyarwa.features.announcements.schemas import Announcement, AnnouncementCreate
from koyarwa.features.announcements.service import AnnouncementService

router = APIRouter(prefix="/announcements", tags=["announcements"])

ServiceDep = Annotated[AnnouncementService, Depends(get_announcement_service)]


@router.get("", response_model=list[Announcement])
def list_announcements(service: ServiceDep) -> list[Announcement]:
    """Liste les annonces — consommé par le portal."""
    return service.list()


@router.post("", response_model=Announcement, status_code=201)
def create_announcement(payload: AnnouncementCreate, service: ServiceDep) -> Announcement:
    return service.create(payload)
