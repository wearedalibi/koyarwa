from koyarwa.core.security import hash_password, verify_password
from koyarwa.features.identity.models import User
from koyarwa.features.identity.repository import UserRepository
from koyarwa.features.identity.schemas import UserCreate


class UserService:
    """Logique des comptes — création (mot de passe haché) et authentification."""

    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def create(self, data: UserCreate, *, is_superuser: bool = False) -> User:
        user = User(
            username=data.username,
            email=data.email,
            password_hash=hash_password(data.password),
            first_name=data.first_name,
            last_name=data.last_name,
            email_visibility=data.email_visibility,
            city=data.city,
            country=data.country,
            timezone=data.timezone,
            description=data.description,
            lang=data.lang,
            is_active=True,
            is_superuser=is_superuser,
        )
        return await self._repository.add(user)

    async def create_prehashed(self, *, is_superuser: bool = False, **fields: str) -> User:
        """Crée un utilisateur dont le mot de passe est **déjà haché**.

        `fields` porte les colonnes du compte, dont `password_hash` — utile quand le
        hachage a eu lieu plus tôt (ex. étape d'assistant précédente) pour ne jamais
        conserver le mot de passe en clair entre-temps.
        """
        user = User(is_active=True, is_superuser=is_superuser, **fields)
        return await self._repository.add(user)

    async def authenticate(self, username: str, password: str) -> User | None:
        """Renvoie l'utilisateur si les identifiants sont valides et le compte actif."""
        user = await self._repository.get_by_username(username)
        if user is None or not user.is_active:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    async def count(self) -> int:
        return await self._repository.count()
