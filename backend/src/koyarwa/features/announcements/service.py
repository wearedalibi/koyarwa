from koyarwa.features.announcements.repository import AnnouncementRepository
from koyarwa.features.announcements.schemas import Announcement, AnnouncementCreate


class AnnouncementService:
    """Logique métier des annonces — indépendante du canal (API JSON ou admin HTML).

    C'est le point de partage : l'API REST (qui alimente le portal) et le
    back-office admin consomment tous deux ce service.
    """

    def __init__(self, repository: AnnouncementRepository) -> None:
        self._repository = repository

    def list(self) -> list[Announcement]:
        return self._repository.list()

    def create(self, data: AnnouncementCreate) -> Announcement:
        return self._repository.create(data)
