from pydantic import SecretStr
from pydantic_settings import SettingsConfigDict

from koyarwa.core.config.base import SectionSettings


class AdminSettings(SectionSettings):
    """Back-office admin — préfixe `ADMIN_`.

    Auth par session (cookie signé). Compte unique piloté par l'environnement ;
    à remplacer par de vrais comptes en base pour la production.
    """

    model_config = SettingsConfigDict(env_prefix="ADMIN_")

    username: str = "admin"
    password: SecretStr = SecretStr("admin")
    # Clé de signature des cookies de session — À SURCHARGER en prod
    # (valeur longue et aléatoire, ex. `openssl rand -hex 32`).
    session_secret: SecretStr = SecretStr("dev-insecure-change-me")
    session_cookie: str = "koyarwa_admin"
    session_max_age: int = 60 * 60 * 8  # 8 h
