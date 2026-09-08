from datetime import datetime

from pydantic import BaseModel, Field


class AnnouncementCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Titre de l'annonce")
    body: str = Field(..., min_length=1, description="Contenu de l'annonce")


class Announcement(BaseModel):
    id: int
    title: str
    body: str
    created_at: datetime
