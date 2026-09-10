from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings

from koyarwa.core.config.admin import AdminSettings
from koyarwa.core.config.api import ApiSettings
from koyarwa.core.config.app import AppSettings
from koyarwa.core.config.cors import CORSSettings
from koyarwa.core.config.database import DatabaseSettings
from koyarwa.core.config.ratelimit import RateLimitSettings


class Settings(BaseSettings):
    """Configuration racine : composition des sections par domaine.

    Chaque section se charge depuis l'environnement avec son propre préfixe ; on
    n'accède jamais à une valeur en dur mais via `settings.<section>.<champ>`.
    """

    app: AppSettings = Field(default_factory=AppSettings)
    admin: AdminSettings = Field(default_factory=AdminSettings)
    api: ApiSettings = Field(default_factory=ApiSettings)
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    cors: CORSSettings = Field(default_factory=CORSSettings)
    ratelimit: RateLimitSettings = Field(default_factory=RateLimitSettings)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Instance unique (mémoïsée) — le `.env` n'est lu qu'une fois par process."""
    return Settings()


settings = get_settings()
