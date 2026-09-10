import pytest
from pydantic import ValidationError

from koyarwa.core.config.cors import CORSSettings


def test_refuse_wildcard_avec_credentials():
    with pytest.raises(ValidationError):
        CORSSettings(origins=["*"], allow_credentials=True)


def test_wildcard_tolere_sans_credentials():
    settings = CORSSettings(origins=["*"], allow_credentials=False)
    assert settings.origins == ["*"]


def test_origines_explicites_avec_credentials_ok():
    settings = CORSSettings(origins=["https://app.example.com"], allow_credentials=True)
    assert settings.allow_credentials is True
