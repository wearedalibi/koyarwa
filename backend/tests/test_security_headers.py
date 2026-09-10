from fastapi.testclient import TestClient

from koyarwa.main import app


def test_en_tetes_de_securite_presents():
    with TestClient(app) as client:
        r = client.get("/api/v1/health")
    assert r.headers["x-content-type-options"] == "nosniff"
    assert r.headers["x-frame-options"] == "DENY"
    assert r.headers["referrer-policy"] == "strict-origin-when-cross-origin"
    csp = r.headers["content-security-policy"]
    assert "frame-ancestors 'none'" in csp
    assert "object-src 'none'" in csp
    assert "form-action 'self'" in csp


def test_hsts_absent_hors_prod():
    with TestClient(app) as client:
        r = client.get("/api/v1/health")
    assert "strict-transport-security" not in {k.lower() for k in r.headers}
