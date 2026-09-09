from __future__ import annotations

from typing import Protocol

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from koyarwa.features.identity.models import User


class UserRepository(Protocol):
    """Port de persistance des comptes (consommé par le service)."""

    async def get_by_username(self, username: str) -> User | None: ...

    async def get_by_email(self, email: str) -> User | None: ...

    async def add(self, user: User) -> User: ...

    async def count(self) -> int: ...


class SqlUserRepository:
    """Implémentation SQLAlchemy async."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_username(self, username: str) -> User | None:
        result = await self._session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self._session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def add(self, user: User) -> User:
        self._session.add(user)
        await self._session.flush()
        return user

    async def count(self) -> int:
        result = await self._session.execute(select(func.count()).select_from(User))
        return int(result.scalar_one())
