import re
from types import SimpleNamespace

import pytest

from koyarwa.bootstrap import gate


class _StubUserService:
    """Faux service d'authentification : un unique super-admin `admin` / `admin`.

    Évite une vraie base pour les tests du back-office (le login s'authentifie
    désormais sur le super-administrateur en base).
    """

    async def authenticate(self, username: str, password: str) -> object | None:
        if username == "admin" and password == "admin":
            return SimpleNamespace(username="admin", is_superuser=True, is_active=True)
        return None


@pytest.fixture(autouse=True)
def _seed_admin_user():
    """Remplace le service d'auth admin par un stub (super-admin admin/admin)."""
    from koyarwa.features.identity.ports import get_user_service
    from koyarwa.main import app

    app.dependency_overrides[get_user_service] = lambda: _StubUserService()
    yield
    app.dependency_overrides.pop(get_user_service, None)


@pytest.fixture(autouse=True)
def _reset_login_throttle():
    """Réinitialise le verrou anti-force-brute entre les tests (état de process)."""
    from koyarwa.admin import auth

    auth.login_throttle.reset()
    yield
    auth.login_throttle.reset()


@pytest.fixture
def csrf():
    """Extrait le jeton CSRF (champ caché) d'une page pour rejouer un POST valide."""

    def _token(client, url: str) -> str:
        html = client.get(url).text
        match = re.search(r'name="csrf_token" value="([^"]+)"', html)
        assert match, f"aucun champ csrf_token sur {url}"
        return match.group(1)

    return _token


@pytest.fixture(autouse=True)
def _installed(monkeypatch):
    """Par défaut, les tests s'exécutent comme si l'instance était installée.

    (Sinon le setup-gate redirigerait toutes les requêtes vers `/setup`.)
    Les tests du gate lui-même redéfinissent ce comportement.
    """
    monkeypatch.setattr(gate, "is_installed", lambda: True)


@pytest.fixture(autouse=True)
def _instance_dir(tmp_path, monkeypatch):
    """Isole chaque test : dossier d'instance (config, jeton) dans un tmp jetable."""
    monkeypatch.setenv("KOYARWA_INSTANCE_DIR", str(tmp_path / "instance"))
