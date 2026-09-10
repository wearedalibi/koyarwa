from typing import Annotated, Self

from pydantic import field_validator, model_validator
from pydantic_settings import NoDecode, SettingsConfigDict

from koyarwa.core.config.base import SectionSettings


class CORSSettings(SectionSettings):
    """Politique CORS — préfixe `CORS_`.

    `origins` accepte une liste séparée par des virgules dans l'env
    (ex. `CORS_ORIGINS=http://localhost:5173,https://app.example.com`).
    `NoDecode` désactive le décodage JSON automatique pour laisser le validateur
    faire le split.
    """

    model_config = SettingsConfigDict(env_prefix="CORS_")

    # Champ pydantic : le défaut mutable est copié en toute sécurité par pydantic.
    origins: Annotated[list[str], NoDecode] = ["http://localhost:5173"]  # noqa: RUF012
    allow_credentials: bool = True

    @field_validator("origins", mode="before")
    @classmethod
    def _split(cls, value: object) -> object:
        if isinstance(value, str):
            return [o.strip() for o in value.split(",") if o.strip()]
        return value

    @model_validator(mode="after")
    def _reject_wildcard_with_credentials(self) -> Self:
        """Interdit `origins=*` avec `allow_credentials` (combinaison cross-site dangereuse).

        Le navigateur refuse `Access-Control-Allow-Origin: *` avec des identifiants,
        mais Starlette reflèterait alors n'importe quelle origine — équivalent à `*`
        avec credentials. On échoue tôt plutôt que d'ouvrir l'API à toute origine.
        """
        if self.allow_credentials and "*" in self.origins:
            raise ValueError(
                "CORS : '*' comme origine est interdit avec allow_credentials=True. "
                "Listez explicitement les origines autorisées (CORS_ORIGINS)."
            )
        return self
