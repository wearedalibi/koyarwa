from fastapi.testclient import TestClient

from koyarwa.main import app


def test_lifespan_demarre_et_repond():
    """Le lifespan ne casse pas le démarrage et l'app répond."""
    with TestClient(app) as client:  # entre/sort du lifespan
        res = client.get("/api/v1/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
