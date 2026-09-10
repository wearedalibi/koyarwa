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
        # super-admin en base simulé par le stub d'auth (admin / admin)
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


def test_verrou_apres_trop_d_echecs(csrf):
    with TestClient(app) as client:
        token = csrf(client, "/admin/login")
        # 5 échecs autorisés (401), puis le compte est verrouillé (429).
        for _ in range(5):
            r = client.post(
                "/admin/login",
                data={"username": "admin", "password": "faux", "csrf_token": token},
                follow_redirects=False,
            )
            assert r.status_code == 401
        locked = client.post(
            "/admin/login",
            data={"username": "admin", "password": "faux", "csrf_token": token},
            follow_redirects=False,
        )
        assert locked.status_code == 429
        # Même avec le bon mot de passe, le verrou tient.
        still = client.post(
            "/admin/login",
            data={"username": "admin", "password": "admin", "csrf_token": token},
            follow_redirects=False,
        )
        assert still.status_code == 429
