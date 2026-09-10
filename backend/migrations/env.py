"""Environnement Alembic (async).

L'URL de connexion n'est pas écrite dans alembic.ini : elle est résolue au moment de
la migration via `koyarwa.core.db.resolve_db_url` (configuration d'instance si installée,
sinon environnement). Les migrations restent donc valables pour PostgreSQL et MySQL.
"""

from __future__ import annotations

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from koyarwa.core.db import Base, resolve_db_url

# Importer les modèles pour peupler Base.metadata (nécessaire à l'autogénération).
from koyarwa.features.identity import models  # noqa: F401
from koyarwa.features.site import models as site_models  # noqa: F401

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Migrations en mode « offline » (génère le SQL sans connexion)."""
    context.configure(
        url=resolve_db_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def _do_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Migrations en mode « online » (via une connexion async au moteur)."""
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = resolve_db_url()
    connectable = async_engine_from_config(
        configuration, prefix="sqlalchemy.", poolclass=pool.NullPool
    )
    async with connectable.connect() as connection:
        await connection.run_sync(_do_migrations)
    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
