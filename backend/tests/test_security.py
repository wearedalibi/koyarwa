from koyarwa.core.security import hash_password, verify_password


def test_hachage_puis_verification():
    hashed = hash_password("s3cret-pass")
    assert hashed != "s3cret-pass"
    assert verify_password("s3cret-pass", hashed) is True
    assert verify_password("mauvais", hashed) is False


def test_deux_hachages_du_meme_mot_de_passe_different():
    # Sel aléatoire → deux hachages distincts pour un même mot de passe.
    assert hash_password("meme-pass") != hash_password("meme-pass")
