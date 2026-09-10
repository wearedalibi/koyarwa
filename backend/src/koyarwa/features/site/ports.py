from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from koyarwa.core.db import get_session
from koyarwa.features.site.repository import SqlSiteRepository
from koyarwa.features.site.service import SiteService


def get_site_service(session: Annotated[AsyncSession, Depends(get_session)]) -> SiteService:
    """Dépendance FastAPI : le service câblé sur le dépôt SQLAlchemy."""
    return SiteService(SqlSiteRepository(session))
