from fastapi.testclient import TestClient

from koyarwa.bootstrap import gate, setup_token
from koyarwa.main import app


def test_l_assistant_exige_le_jeton(monkeypatch, csrf):
    monkeypatch.setattr(gate, "is_installed", lambda: False)
    setup_token.clear_token()

    with TestClient(app) as client:
        # Sans jeton validé, /setup montre la saisie du jeton (pas l'étape langue).
        first = client.get("/setup")
        assert first.status_code == 200
        assert 'name="token"' in first.text

        token = setup_token.get_or_create_token()
        csrf_token = csrf(client, "/setup")

        # Mauvais jeton → refusé (le CSRF est valide : c'est bien le jeton qui échoue).
        bad = client.post(
            "/setup/token",
            data={"token": "mauvais", "csrf_token": csrf_token},
            follow_redirects=False,
        )
        assert bad.status_code == 403

        # Une étape ne peut pas être atteinte sans jeton validé.
        skipped = client.get("/setup/database", follow_redirects=False)
        assert skipped.status_code == 303
        assert skipped.headers["location"] == "/setup"

        # Bon jeton → validé, puis l'étape langue devient accessible.
        ok = client.post(
            "/setup/token",
            data={"token": token, "csrf_token": csrf_token},
            follow_redirects=False,
        )
        assert ok.status_code == 303
        page = client.get("/setup")
        assert 'name="language"' in page.text
