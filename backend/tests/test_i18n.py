from koyarwa.core.i18n import (
    DEFAULT_LANGUAGE,
    SUPPORTED_LANGUAGES,
    normalize_locale,
    translate,
)


def test_langues_supportees():
    assert DEFAULT_LANGUAGE == "fr"
    assert set(SUPPORTED_LANGUAGES) == {"fr", "en", "de"}


def test_normalisation():
    assert normalize_locale("en-US") == "en"
    assert normalize_locale("de_DE") == "de"
    assert normalize_locale("es") == "fr"  # non supportée → défaut
    assert normalize_locale(None) == "fr"


def test_traduction_et_replis():
    assert translate("admin.login.title", "fr") == "Connexion"
    assert translate("admin.login.title", "en") == "Sign in"
    assert translate("admin.login.title", "de") == "Anmelden"
    # clé absente → repli sur la clé brute
    assert translate("cle.absente", "en") == "cle.absente"
    # langue non supportée → repli sur le français
    assert translate("admin.logout", "es") == "Déconnexion"
