from fastapi.testclient import TestClient

from koyarwa.bootstrap import gate, service
from koyarwa.main import app

_DB = {
    "engine": "postgresql",
    "host": "h",
    "port": "5432",
    "user": "u",
    "password": "p",
    "name": "n",
}
_ADMIN = {
    "first_name": "Ada",
    "last_name": "Lovelace",
    "username": "admin",
    "email": "admin@ecole.fr",
    "password": "S3cret-passx",
    "email_visibility": "hidden",
    "city": "Lyon",
    "country": "France",
    "timezone": "Europe/Paris",
    "description": "",
}


def test_flux_admin_puis_site(monkeypatch, csrf):
    monkeypatch.setattr(gate, "is_installed", lambda: False)

    async def _connexion_ok(db):
        return (True, "")

    monkeypatch.setattr(service, "test_connection", _connexion_ok)

    with TestClient(app) as client:
        token = csrf(client, "/setup")
        client.post("/setup", data={"language": "fr", "csrf_token": token}, follow_redirects=False)
        client.post(
            "/setup/database", data={**_DB, "csrf_token": token}, follow_redirects=False
        )

        # Étape admin : champs de profil présents.
        admin_page = client.get("/setup/admin")
        assert admin_page.status_code == 200
        for field in (
            'name="first_name"',
            'name="last_name"',
            'name="email_visibility"',
            'name="city"',
            'name="country"',
            'name="timezone"',
            'name="description"',
        ):
            assert field in admin_page.text

        # Soumission admin valide → passe à l'étape site (pas de finalisation ici).
        posted = client.post(
            "/setup/admin", data={**_ADMIN, "csrf_token": token}, follow_redirects=False
        )
        assert posted.status_code == 303
        assert posted.headers["location"] == "/setup/site"

        # Étape site : champs de configuration du site.
        site_page = client.get("/setup/site")
        assert site_page.status_code == 200
        for field in (
            'name="full_name"',
            'name="short_name"',
            'name="auth_method"',
            'name="noreply_email"',
            'name="support_email"',
        ):
            assert field in site_page.text
        assert 'value="Europe/Paris"' in site_page.text


def test_mot_de_passe_faible_refuse_a_l_etape_admin(monkeypatch, csrf):
    monkeypatch.setattr(gate, "is_installed", lambda: False)

    async def _connexion_ok(db):
        return (True, "")

    monkeypatch.setattr(service, "test_connection", _connexion_ok)

    with TestClient(app) as client:
        token = csrf(client, "/setup")
        client.post("/setup", data={"language": "fr", "csrf_token": token}, follow_redirects=False)
        client.post(
            "/setup/database", data={**_DB, "csrf_token": token}, follow_redirects=False
        )
        weak = client.post(
            "/setup/admin",
            data={**_ADMIN, "password": "faible", "csrf_token": token},
            follow_redirects=False,
        )
    assert weak.status_code == 400
