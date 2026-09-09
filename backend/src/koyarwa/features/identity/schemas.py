from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=1, max_length=150)
    email: EmailStr
    password: str = Field(min_length=8, description="Mot de passe en clair (haché avant stockage)")
    first_name: str = Field(default="", max_length=150)
    last_name: str = Field(default="", max_length=150)
    lang: str = Field(default="fr", max_length=8)


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
