from pydantic_settings import SettingsConfigDict

from koyarwa.core.config.base import SectionSettings


class RateLimitSettings(SectionSettings):
    """Limitation de débit de l'API — préfixe `RATELIMIT_`.

    Défense en profondeur : fenêtre glissante par IP cliente, en mémoire du
    process. Suffisant pour un déploiement mono-instance ; à remplacer par un
    store partagé (Redis) si l'API est un jour répliquée.
    """

    model_config = SettingsConfigDict(env_prefix="RATELIMIT_")

    enabled: bool = True
    requests: int = 120  # requêtes autorisées par fenêtre et par client
    window_seconds: int = 60
    # Derrière un reverse-proxy (nginx), l'IP directe est celle du proxy : activer
    # pour dériver l'IP cliente réelle de `X-Forwarded-For`. Ne l'activer QUE si un
    # proxy de confiance ajoute cet en-tête (sinon un client peut usurper son IP).
    trust_proxy: bool = False
