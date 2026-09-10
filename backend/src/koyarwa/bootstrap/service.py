from __future__ import annotations

from pathlib import Path

from alembic import command
from alembic.config import Config
from anyio import to_thread
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

from koyarwa.bootstrap.setup_token import clear_token
from koyarwa.core.config.database import build_async_url
from koyarwa.core.db import get_sessionmaker, reset_engine
from koyarwa.core.instance import DatabaseConfig, InstanceConfig, save
from koyarwa.features.identity.repository import SqlUserRepository
from koyarwa.features.identity.schemas import UserCreate
from koyarwa.features.identity.service import UserService

_BACKEND_ROOT = Path(__file__).resolve().parents[3]  # .../backend


async def test_connection(db: DatabaseConfig) -> tuple[bool, str]:
    """Teste la connexion à la base ; renvoie `(ok, message_d_erreur)`."""
    url = build_async_url(
        engine=db.engine,
        host=db.host,
        port=db.port,
        user=db.user,
        password=db.password,
        name=db.name,
    )
    engine = create_async_engine(url, poolclass=NullPool)
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return True, ""
    except Exception as exc:  # l'échec est rapporté à l'installateur
        return False, str(exc)
    finally:
        await engine.dispose()


def _run_migrations_sync() -> None:
    cfg = Config(str(_BACKEND_ROOT / "alembic.ini"))
    cfg.set_main_option("script_location", str(_BACKEND_ROOT / "migrations"))
    command.upgrade(cfg, "head")


async def apply_migrations() -> None:
    """Applique les migrations (dans un thread : Alembic gère sa propre boucle async)."""
    await to_thread.run_sync(_run_migrations_sync)


async def finalize_install(*, language: str, database: DatabaseConfig, admin: UserCreate) -> None:
    """Écrit la config, applique le schéma, crée le super-admin, pose le verrou."""
    # 1. config (non verrouillée) → la base saisie devient la base active
    save(InstanceConfig(installed=False, language=language, database=database))
    reset_engine()
    # 2. schéma
    await apply_migrations()
    # 3. compte super-administrateur
    async with get_sessionmaker()() as session:
        await UserService(SqlUserRepository(session)).create(admin, is_superuser=True)
        await session.commit()
    # 4. verrou d'installation + invalidation du jeton
    save(InstanceConfig(installed=True, language=language, database=database))
    clear_token()
