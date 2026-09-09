import pytest

from koyarwa.bootstrap import gate


@pytest.fixture(autouse=True)
def _installed(monkeypatch):
    """Par défaut, les tests s'exécutent comme si l'instance était installée.

    (Sinon le setup-gate redirigerait toutes les requêtes vers `/setup`.)
    Les tests du gate lui-même redéfinissent ce comportement.
    """
    monkeypatch.setattr(gate, "is_installed", lambda: True)
