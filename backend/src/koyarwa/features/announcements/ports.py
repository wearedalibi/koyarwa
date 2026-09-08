from functools import lru_cache

from koyarwa.features.announcements.repository import (
    AnnouncementRepository,
    InMemoryAnnouncementRepository,
)
from koyarwa.features.announcements.service import AnnouncementService


@lru_cache(maxsize=1)
def _repository() -> AnnouncementRepository:
    """Dépôt singleton (en mémoire) partagé par tous les canaux du process.

    Remplacer l'implémentation par un dépôt SQLAlchemy pour persister en base.
    """
    return InMemoryAnnouncementRepository()


def get_announcement_service() -> AnnouncementService:
    """Dépendance FastAPI : le service câblé sur le dépôt courant."""
    return AnnouncementService(_repository())
