from fastapi.testclient import TestClient

from koyarwa.main import app


def test_liste_et_creation_annonce():
    with TestClient(app) as client:
        created = client.post(
            "/api/v1/announcements",
            json={"title": "Rentrée", "body": "Le 1er septembre."},
        )
        assert created.status_code == 201
        data = created.json()
        assert data["id"] >= 1
        assert data["title"] == "Rentrée"
        assert "created_at" in data

        listed = client.get("/api/v1/announcements")
        assert listed.status_code == 200
        assert "Rentrée" in [a["title"] for a in listed.json()]


def test_creation_refuse_titre_vide():
    with TestClient(app) as client:
        res = client.post("/api/v1/announcements", json={"title": "", "body": "x"})
    assert res.status_code == 422
