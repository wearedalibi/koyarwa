from fastapi.testclient import TestClient

from koyarwa.main import app


def test_page_admin_protegee_redirige_vers_login():
    with TestClient(app) as client:
        res = client.get("/admin/announcements", follow_redirects=False)
    assert res.status_code == 303
    assert res.headers["location"] == "/admin/login"


def test_login_invalide_reste_401(csrf):
    with TestClient(app) as client:
        token = csrf(client, "/admin/login")
        res = client.post(
            "/admin/login",
            data={"username": "admin", "password": "mauvais", "csrf_token": token},
            follow_redirects=False,
        )
    assert res.status_code == 401


def test_login_puis_acces_page_protegee(csrf):
    with TestClient(app) as client:
        # défauts ADMIN_USERNAME / ADMIN_PASSWORD = admin / admin
        token = csrf(client, "/admin/login")
        ok = client.post(
            "/admin/login",
            data={"username": "admin", "password": "admin", "csrf_token": token},
            follow_redirects=False,
        )
        assert ok.status_code == 303
        assert ok.headers["location"] == "/admin/announcements"

        # le cookie de session est conservé par le client → accès autorisé
        page = client.get("/admin/announcements")
        assert page.status_code == 200
        assert "Annonces" in page.text
