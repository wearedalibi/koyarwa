from fastapi.testclient import TestClient

from koyarwa.bootstrap import gate, service
from koyarwa.main import app


def test_etape_admin_expose_les_champs_de_profil(monkeypatch, csrf):
    monkeypatch.setattr(gate, "is_installed", lambda: False)

    async def _connexion_ok(db):
        return (True, "")

    monkeypatch.setattr(service, "test_connection", _connexion_ok)

    with TestClient(app) as client:
        token = csrf(client, "/setup")
        client.post("/setup", data={"language": "fr", "csrf_token": token}, follow_redirects=False)
        client.post(
            "/setup/database",
            data={
                "engine": "postgresql",
                "host": "h",
                "port": "5432",
                "user": "u",
                "password": "p",
                "name": "n",
                "csrf_token": token,
            },
            follow_redirects=False,
        )
        page = client.get("/setup/admin")

    assert page.status_code == 200
    for field in (
        'name="first_name"',
        'name="last_name"',
        'name="email_visibility"',
        'name="city"',
        'name="country"',
        'name="timezone"',
        'name="description"',
    ):
        assert field in page.text
    # Le sélecteur de fuseaux est bien peuplé.
    assert 'value="Europe/Paris"' in page.text
