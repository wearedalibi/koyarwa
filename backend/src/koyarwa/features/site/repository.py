from __future__ import annotations

from typing import Protocol

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from koyarwa.features.site.models import Site


class SiteRepository(Protocol):
    """Port de persistance du site (enregistrement unique)."""

    async def get(self) -> Site | None: ...

    async def add(self, site: Site) -> Site: ...


class SqlSiteRepository:
    """Implémentation SQLAlchemy async."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self) -> Site | None:
        result = await self._session.execute(select(Site).order_by(Site.id).limit(1))
        return result.scalar_one_or_none()

    async def add(self, site: Site) -> Site:
        self._session.add(site)
        await self._session.flush()
        return site
