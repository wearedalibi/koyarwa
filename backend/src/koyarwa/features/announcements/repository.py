from __future__ import annotations

from datetime import UTC, datetime
from typing import Protocol

from koyarwa.features.announcements.schemas import Announcement, AnnouncementCreate


class AnnouncementRepository(Protocol):
    """Port de persistance des annonces (consommé par le service)."""

    def list(self) -> list[Announcement]: ...

    def create(self, data: AnnouncementCreate) -> Announcement: ...


class InMemoryAnnouncementRepository:
    """Implémentation en mémoire — démo, sans base (l'app tourne sans Postgres).

    Pour une version durable : implémenter le même port avec SQLAlchemy en
    s'appuyant sur `core.db` (un modèle + la session async), sans toucher au
    service ni aux routers.
    """

    def __init__(self) -> None:
        self._items: list[Announcement] = []
        self._seq = 0

    def list(self) -> list[Announcement]:
        return list(reversed(self._items))  # plus récentes d'abord

    def create(self, data: AnnouncementCreate) -> Announcement:
        self._seq += 1
        item = Announcement(
            id=self._seq,
            title=data.title,
            body=data.body,
            created_at=datetime.now(UTC),
        )
        self._items.append(item)
        return item
