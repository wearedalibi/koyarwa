from pydantic import SecretStr
from pydantic_settings import SettingsConfigDict

from koyarwa.core.config.base import SectionSettings


class ApiSettings(SectionSettings):
    """API JSON du portal — préfixe `API_`."""

    model_config = SettingsConfigDict(env_prefix="API_")

    # Jeton de service (Bearer) protégeant l'API. Vide = API ouverte (dev) ; à
    # définir en production tant que l'authentification par utilisateur du portal
    # (Phase 1) n'est pas en place. Un avertissement est émis au démarrage si
    # l'API tourne ouverte en prod.
    token: SecretStr = SecretStr("")
