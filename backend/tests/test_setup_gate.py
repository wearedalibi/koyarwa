from fastapi.testclient import TestClient

from koyarwa.bootstrap import gate
from koyarwa.main import app


def test_non_installe_redirige_tout_vers_setup(monkeypatch):
    monkeypatch.setattr(gate, "is_installed", lambda: False)
    with TestClient(app) as client:
        res = client.get("/api/v1/health", follow_redirects=False)
    assert res.status_code == 307
    assert res.headers["location"] == "/setup"


def test_non_installe_assistant_accessible(monkeypatch):
    monkeypatch.setattr(gate, "is_installed", lambda: False)
    with TestClient(app) as client:
        res = client.get("/setup", follow_redirects=False)
    assert res.status_code == 200
    assert "Koyarwa" in res.text


def test_installe_ferme_l_assistant():
    # le fixture autouse simule « installé »
    with TestClient(app) as client:
        res = client.get("/setup", follow_redirects=False)
    assert res.status_code == 307
    assert res.headers["location"] == "/admin"
