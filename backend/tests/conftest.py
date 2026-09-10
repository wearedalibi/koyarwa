import re

import pytest

from koyarwa.bootstrap import gate


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
