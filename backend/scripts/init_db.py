"""Initialise le schéma de la base à partir des modèles SQLAlchemy.

Usage : uv run python scripts/init_db.py
Script one-shot en moteur synchrone (évite les soucis d'event loop asyncio sous
Windows). Pour un vrai versionnage de schéma, migrer ensuite vers Alembic.

Chaque feature qui possède des modèles doit être importée ci-dessous pour que
ses tables soient enregistrées sur `Base.metadata` avant `create_all`. Exemple :

    from koyarwa.features.<feature>.models import <Model>  # noqa: F401
"""

from sqlalchemy import create_engine

from koyarwa.core.config import settings
from koyarwa.core.db import Base


def main() -> None:
    engine = create_engine(settings.db.url, future=True)
    with engine.begin() as conn:
        Base.metadata.create_all(conn)
    tables = ", ".join(sorted(Base.metadata.tables)) or "(aucune table déclarée)"
    print(f"Base initialisée. Tables : {tables}")


if __name__ == "__main__":
    main()
