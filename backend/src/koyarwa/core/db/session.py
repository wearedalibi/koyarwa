from collections.abc import AsyncGenerator
from functools import lru_cache

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from koyarwa.core.config import settings


def resolve_db_url() -> str:
    """URL de connexion : config d'instance si installée, sinon l'environnement (dev)."""
    from koyarwa.core.instance import config as instance_config

    return instance_config.database_url() or settings.db.url


@lru_cache(maxsize=1)
def get_engine() -> AsyncEngine:
    """Moteur async créé **paresseusement** (au premier accès, pas à l'import).

    Ainsi l'application peut démarrer en mode installation, sans base configurée :
    aucune connexion n'est tentée tant qu'une feature n'a pas besoin de la base.
    """
    return create_async_engine(
        resolve_db_url(),
        echo=settings.db.echo,
        pool_size=settings.db.pool_size,
        max_overflow=settings.db.max_overflow,
        pool_pre_ping=settings.db.pool_pre_ping,
        future=True,
    )


@lru_cache(maxsize=1)
def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(get_engine(), expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dépendance FastAPI : fournit une session async par requête."""
    async with get_sessionmaker()() as session:
        yield session


def reset_engine() -> None:
    """Oublie le moteur en cache — à appeler après (re)configuration de la base."""
    get_engine.cache_clear()
    get_sessionmaker.cache_clear()
