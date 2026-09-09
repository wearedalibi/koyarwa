from typing import Literal

from pydantic import SecretStr
from pydantic_settings import SettingsConfigDict
from sqlalchemy import URL

from koyarwa.core.config.base import SectionSettings

# Driver SQLAlchemy async par moteur (pilotes purs Python, installables partout).
_ASYNC_DRIVERS: dict[str, str] = {
    "postgresql": "postgresql+psycopg",
    "mysql": "mysql+aiomysql",
}
_DEFAULT_PORTS: dict[str, int] = {"postgresql": 5432, "mysql": 3306}


def build_async_url(
    *,
    engine: str,
    host: str,
    port: int | None,
    user: str,
    password: str,
    name: str,
) -> str:
    """Compose une URL SQLAlchemy async pour le moteur donné.

    Passe par `URL.create` pour un échappement correct (mots de passe à caractères
    spéciaux inclus).
    """
    return URL.create(
        drivername=_ASYNC_DRIVERS[engine],
        username=user,
        password=password,
        host=host,
        port=port if port is not None else _DEFAULT_PORTS[engine],
        database=name,
    ).render_as_string(hide_password=False)


class DatabaseSettings(SectionSettings):
    """Connexion à la base — préfixe `DB_`. Moteur **PostgreSQL** ou **MySQL**.

    L'URL n'est jamais écrite en dur : elle est composée à partir des composants.
    Pour une instance installée, la connexion provient plutôt de la configuration
    d'instance (voir `core.instance`) ; ces valeurs servent de repli en développement.
    """

    model_config = SettingsConfigDict(env_prefix="DB_")

    engine: Literal["postgresql", "mysql"] = "postgresql"
    host: str = "localhost"
    port: int | None = None  # None → port par défaut du moteur
    user: str = "koyarwa"
    password: SecretStr = SecretStr("koyarwa")
    name: str = "koyarwa"

    # Pool / debug
    echo: bool = False
    pool_size: int = 5
    max_overflow: int = 10
    pool_pre_ping: bool = True

    @property
    def resolved_port(self) -> int:
        return self.port if self.port is not None else _DEFAULT_PORTS[self.engine]

    @property
    def driver(self) -> str:
        """Driver SQLAlchemy async correspondant au moteur choisi."""
        return _ASYNC_DRIVERS[self.engine]

    @property
    def url(self) -> str:
        """DSN SQLAlchemy async, composé à partir des composants."""
        return build_async_url(
            engine=self.engine,
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password.get_secret_value(),
            name=self.name,
        )
