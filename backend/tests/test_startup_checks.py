import pytest

from koyarwa.core.security import checks


def test_prod_installee_refuse_la_cle_d_usine(monkeypatch):
    monkeypatch.setattr(checks.settings.app, "env", "prod")
    monkeypatch.setattr(checks, "is_installed", lambda: True)
    # Aucune clé d'instance (dossier tmp vide) → clé effective = valeur d'usine.
    with pytest.raises(RuntimeError):
        checks.check_startup_security()


def test_dev_avertit_sans_bloquer(monkeypatch):
    monkeypatch.setattr(checks.settings.app, "env", "dev")
    monkeypatch.setattr(checks, "is_installed", lambda: True)
    checks.check_startup_security()  # ne lève pas


def test_prod_non_installee_ne_bloque_pas(monkeypatch):
    # Avant installation, l'assistant doit pouvoir tourner malgré la clé d'usine.
    monkeypatch.setattr(checks.settings.app, "env", "prod")
    monkeypatch.setattr(checks, "is_installed", lambda: False)
    checks.check_startup_security()  # ne lève pas
