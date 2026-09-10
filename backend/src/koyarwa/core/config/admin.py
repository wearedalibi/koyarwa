from pydantic import SecretStr
from pydantic_settings import SettingsConfigDict

from koyarwa.core.config.base import SectionSettings


class AdminSettings(SectionSettings):
    """Back-office admin — préfixe `ADMIN_`.

    Auth par session (cookie signé). Les identifiants ne vivent plus ici : la
    connexion s'authentifie sur le **super-administrateur en base** créé lors de
    l'installation (cf. `admin/auth.py` et `bootstrap/service.py`).
    """

    model_config = SettingsConfigDict(env_prefix="ADMIN_")

    # Clé de signature des cookies de session. Valeur d'usine pour le dev
    # uniquement : une clé aléatoire est générée à l'installation et la remplace
    # (cf. `resolve_session_secret`). À SURCHARGER hors installation assistée.
    session_secret: SecretStr = SecretStr("dev-insecure-change-me")
    session_cookie: str = "koyarwa_admin"
    session_max_age: int = 60 * 60 * 8  # 8 h
