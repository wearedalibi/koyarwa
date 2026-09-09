import pytest
from pydantic import ValidationError

from koyarwa.features.identity.models import User
from koyarwa.features.identity.schemas import UserCreate
from koyarwa.features.identity.service import UserService


def test_mot_de_passe_faible_refuse():
    with pytest.raises(ValidationError):
        UserCreate(username="admin", email="admin@ecole.fr", password="faible")  # trop court
    with pytest.raises(ValidationError):
        # 12 caractères mais un seul type → refusé
        UserCreate(username="admin", email="admin@ecole.fr", password="aaaaaaaaaaaa")


class FakeUserRepository:
    """Dépôt en mémoire pour tester le service sans base."""

    def __init__(self) -> None:
        self._users: list[User] = []
        self._seq = 0

    async def get_by_username(self, username: str) -> User | None:
        return next((u for u in self._users if u.username == username), None)

    async def get_by_email(self, email: str) -> User | None:
        return next((u for u in self._users if u.email == email), None)

    async def add(self, user: User) -> User:
        self._seq += 1
        user.id = self._seq
        self._users.append(user)
        return user

    async def count(self) -> int:
        return len(self._users)


async def test_create_hache_et_authentifie():
    service = UserService(FakeUserRepository())

    user = await service.create(
        UserCreate(username="admin", email="admin@ecole.fr", password="s3cret-pass"),
        is_superuser=True,
    )
    assert user.id == 1
    assert user.is_superuser is True
    assert user.password_hash != "s3cret-pass"
    assert await service.count() == 1

    assert await service.authenticate("admin", "s3cret-pass") is not None
    assert await service.authenticate("admin", "mauvais") is None
    assert await service.authenticate("inconnu", "s3cret-pass") is None
