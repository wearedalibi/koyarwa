import os
import stat

from koyarwa.core.instance import config as ic
from koyarwa.core.instance import resolve_session_secret
from koyarwa.core.instance.storage import write_private_text

_POSIX = os.name != "nt"  # les permissions 0600 ne sont vérifiables que sous POSIX


def test_secret_key_aller_retour(tmp_path, monkeypatch):
    monkeypatch.setenv(ic.INSTANCE_DIR_ENV, str(tmp_path))
    ic.save(ic.InstanceConfig(installed=True, language="fr", secret_key="s3cr3t-genere"))
    assert ic.load().secret_key == "s3cr3t-genere"


def test_resolve_prefere_la_cle_d_instance(tmp_path, monkeypatch):
    monkeypatch.setenv(ic.INSTANCE_DIR_ENV, str(tmp_path))
    # Sans config d'instance : la valeur de repli (env/défaut) est utilisée.
    assert resolve_session_secret("repli") == "repli"
    # Une fois une clé persistée : elle l'emporte.
    ic.save(ic.InstanceConfig(installed=True, language="fr", secret_key="cle-instance"))
    assert resolve_session_secret("repli") == "cle-instance"


def test_config_ecrite_en_0600(tmp_path, monkeypatch):
    monkeypatch.setenv(ic.INSTANCE_DIR_ENV, str(tmp_path))
    ic.save(ic.InstanceConfig(installed=True, language="fr", secret_key="x"))
    assert ic.config_path().is_file()
    if _POSIX:
        assert stat.S_IMODE(ic.config_path().stat().st_mode) == 0o600


def test_write_private_text_cree_et_restreint(tmp_path):
    target = tmp_path / "sous-dossier" / "secret.txt"
    write_private_text(target, "contenu")
    assert target.read_text(encoding="utf-8") == "contenu"
    if _POSIX:
        assert stat.S_IMODE(target.stat().st_mode) == 0o600
        assert stat.S_IMODE(target.parent.stat().st_mode) == 0o700
