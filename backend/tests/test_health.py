from fastapi.testclient import TestClient

from koyarwa import __version__
from koyarwa.main import app


def test_health_repond_ok():
    with TestClient(app) as client:
        res = client.get("/api/v1/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok", "version": __version__}
