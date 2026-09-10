from datetime import datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from koyarwa.core.db import Base


class Site(Base):
    """Configuration du site (enregistrement unique, façon « site » Moodle).

    Tout est rattaché au site : nom, fuseau par défaut, méthode d'authentification,
    adresses e-mail système. Éditable ensuite depuis le back-office.
    """

    __tablename__ = "site"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255))
    short_name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text, default="")
    timezone: Mapped[str] = mapped_column(String(64), default="UTC")
    #: Méthode d'authentification par défaut (« manual » = comptes créés par l'admin,
    #: « email » = auto-inscription par e-mail). Stockée dès l'installation.
    auth_method: Mapped[str] = mapped_column(String(50), default="manual")
    #: Adresse d'expédition des messages système (no-reply).
    noreply_email: Mapped[str] = mapped_column(String(255), default="")
    #: Adresse de contact du support.
    support_email: Mapped[str] = mapped_column(String(255), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
