from fastapi.testclient import TestClient

from koyarwa.main import app


def test_post_sans_jeton_csrf_est_refuse():
    with TestClient(app) as client:
        res = client.post(
            "/admin/login",
            data={"username": "admin", "password": "admin"},
            follow_redirects=False,
        )
    assert res.status_code == 403


def test_post_avec_mauvais_jeton_csrf_est_refuse(csrf):
    with TestClient(app) as client:
        csrf(client, "/admin/login")  # établit une session dotée d'un jeton
        res = client.post(
            "/admin/login",
            data={"username": "admin", "password": "admin", "csrf_token": "faux"},
            follow_redirects=False,
        )
    assert res.status_code == 403


def test_post_avec_bon_jeton_csrf_passe_la_garde(csrf):
    with TestClient(app) as client:
        token = csrf(client, "/admin/login")
        # Identifiants erronés → 401 : la garde CSRF a laissé passer, l'auth a tranché.
        res = client.post(
            "/admin/login",
            data={"username": "admin", "password": "mauvais", "csrf_token": token},
            follow_redirects=False,
        )
    assert res.status_code == 401


def test_jeton_csrf_accepte_dans_l_entete(csrf):
    with TestClient(app) as client:
        token = csrf(client, "/admin/login")
        res = client.post(
            "/admin/login",
            data={"username": "admin", "password": "mauvais"},
            headers={"X-CSRF-Token": token},
            follow_redirects=False,
        )
    assert res.status_code == 401
