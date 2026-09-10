import re
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

#: Visibilité de l'adresse e-mail sur le profil.
EmailVisibility = Literal["hidden", "public", "members"]


class UserCreate(BaseModel):
    username: str = Field(min_length=1, max_length=150)
    email: EmailStr
    password: str = Field(min_length=10, description="Mot de passe en clair (haché avant stockage)")
    first_name: str = Field(default="", max_length=150)
    last_name: str = Field(default="", max_length=150)
    email_visibility: EmailVisibility = "hidden"
    city: str = Field(default="", max_length=100)
    country: str = Field(default="", max_length=100)
    timezone: str = Field(default="UTC", max_length=64)
    description: str = Field(default="", max_length=2000)
    lang: str = Field(default="fr", max_length=8)

    @field_validator("password")
    @classmethod
    def _complexity(cls, value: str) -> str:
        """Exige un mot de passe « corsé » : au moins 3 types de caractères."""
        categories = sum(
            bool(re.search(pattern, value))
            for pattern in (r"[a-z]", r"[A-Z]", r"\d", r"[^A-Za-z0-9]")
        )
        if categories < 3:
            raise ValueError(
                "Le mot de passe doit mêler au moins 3 types de caractères "
                "(minuscules, majuscules, chiffres, symboles)."
            )
        return value


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    lang: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
