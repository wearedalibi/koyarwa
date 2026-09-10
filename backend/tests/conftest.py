import pytest

from koyarwa.bootstrap import gate


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
