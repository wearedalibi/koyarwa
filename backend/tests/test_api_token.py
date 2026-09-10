from fastapi.testclient import TestClient
from pydantic import SecretStr

from koyarwa.core.config import settings
from koyarwa.main import app


def test_api_ouverte_sans_jeton_configure():
    with TestClient(app) as client:
        r = client.get("/api/v1/announcements")
    assert r.status_code == 200


def test_api_exige_le_jeton_quand_configure(monkeypatch):
    monkeypatch.setattr(settings.api, "token", SecretStr("s3cret-api"))
    with TestClient(app) as client:
        sans = client.get("/api/v1/announcements")
        assert sans.status_code == 401
        avec = client.get(
            "/api/v1/announcements",
            headers={"Authorization": "Bearer s3cret-api"},
        )
        assert avec.status_code == 200


def test_health_reste_public_meme_avec_jeton(monkeypatch):
    monkeypatch.setattr(settings.api, "token", SecretStr("s3cret-api"))
    with TestClient(app) as client:
        r = client.get("/api/v1/health")
    assert r.status_code == 200
