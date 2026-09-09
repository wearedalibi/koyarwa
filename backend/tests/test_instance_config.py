from koyarwa.core.instance import config as ic


def test_non_installe_par_defaut(tmp_path, monkeypatch):
    monkeypatch.setenv(ic.INSTANCE_DIR_ENV, str(tmp_path))
    assert ic.load() is None
    assert ic.is_installed() is False
    assert ic.database_url() is None
    assert ic.instance_language() is None


def test_sauvegarde_puis_chargement(tmp_path, monkeypatch):
    monkeypatch.setenv(ic.INSTANCE_DIR_ENV, str(tmp_path))
    cfg = ic.InstanceConfig(
        installed=True,
        language="de",
        database=ic.DatabaseConfig(
            engine="postgresql",
            host="db",
            port=5432,
            user="u",
            password='p@ss"x',  # caractères spéciaux → doit être échappé dans l'URL
            name="koyarwa",
        ),
    )
    ic.save(cfg)

    assert ic.config_path().is_file()
    assert ic.load() == cfg
    assert ic.is_installed() is True
    assert ic.instance_language() == "de"

    url = ic.database_url()
    assert url.startswith("postgresql+psycopg://u:")
    assert "@db:5432/koyarwa" in url
    assert 'p@ss"x' not in url  # le mot de passe brut n'apparaît pas tel quel
