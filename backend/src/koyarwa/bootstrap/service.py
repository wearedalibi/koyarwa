from __future__ import annotations

import secrets
from pathlib import Path

from alembic import command
from alembic.config import Config
from anyio import to_thread
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

from koyarwa.core.config.database import build_async_url
from koyarwa.core.db import get_sessionmaker, reset_engine
from koyarwa.core.instance import DatabaseConfig, InstanceConfig, save
from koyarwa.features.identity.repository import SqlUserRepository
from koyarwa.features.identity.schemas import UserCreate
from koyarwa.features.identity.service import UserService

_BACKEND_ROOT = Path(__file__).resolve().parents[3]  # .../backend


class InstanceAlreadyInstalledError(RuntimeError):
    """La base cible contient déjà des comptes : on refuse d'installer par-dessus.

    Garde-fou du cas où le verrou fichier (`config.toml`) a disparu mais la base
    existe encore — évite de créer un second super-admin ou d'écraser l'existant.
    """


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
    # Clé de session propre à l'instance, générée maintenant (façon salts WordPress) :
    # elle remplace la valeur par défaut d'usine au prochain démarrage.
    secret_key = secrets.token_urlsafe(48)
    # 1. config (non verrouillée) → la base saisie devient la base active
    save(
        InstanceConfig(
            installed=False, language=language, database=database, secret_key=secret_key
        )
    )
    reset_engine()
    # 2. schéma
    await apply_migrations()
    # 3. compte super-administrateur — jamais par-dessus une base déjà peuplée
    async with get_sessionmaker()() as session:
        users = UserService(SqlUserRepository(session))
        if await users.count() > 0:
            raise InstanceAlreadyInstalledError
        await users.create(admin, is_superuser=True)
        await session.commit()
    # 4. verrou d'installation
    save(
        InstanceConfig(
            installed=True, language=language, database=database, secret_key=secret_key
        )
    )
