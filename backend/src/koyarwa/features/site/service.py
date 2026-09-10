from koyarwa.features.site.models import Site
from koyarwa.features.site.repository import SiteRepository
from koyarwa.features.site.schemas import SiteCreate


class SiteService:
    """Logique du site (création à l'installation, lecture)."""

    def __init__(self, repository: SiteRepository) -> None:
        self._repository = repository

    async def create(self, data: SiteCreate) -> Site:
        return await self._repository.add(Site(**data.model_dump()))

    async def get(self) -> Site | None:
        return await self._repository.get()
