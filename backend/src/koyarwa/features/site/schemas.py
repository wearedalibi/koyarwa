from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

#: Méthode d'authentification par défaut du site.
AuthMethod = Literal["manual", "email"]


class SiteCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=255)
    short_name: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=2000)
    timezone: str = Field(default="UTC", max_length=64)
    auth_method: AuthMethod = "manual"
    noreply_email: str = Field(default="", max_length=255)
    support_email: str = Field(default="", max_length=255)


class SiteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    short_name: str
    description: str
    timezone: str
    auth_method: str
    noreply_email: str
    support_email: str
    created_at: datetime
