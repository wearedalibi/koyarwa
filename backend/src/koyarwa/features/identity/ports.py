from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from koyarwa.core.db import get_session
from koyarwa.features.identity.repository import SqlUserRepository
from koyarwa.features.identity.service import UserService


def get_user_service(session: Annotated[AsyncSession, Depends(get_session)]) -> UserService:
    """Dépendance FastAPI : le service câblé sur le dépôt SQLAlchemy."""
    return UserService(SqlUserRepository(session))
