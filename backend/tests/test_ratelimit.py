from koyarwa.api.ratelimit import SlidingWindowLimiter


def test_bloque_au_dela_de_la_limite():
    limiter = SlidingWindowLimiter(limit=2, window=60)
    assert limiter.allow("ip", now=0.0) is True
    assert limiter.allow("ip", now=0.1) is True
    assert limiter.allow("ip", now=0.2) is False  # 3e requête dans la fenêtre


def test_la_fenetre_glisse():
    limiter = SlidingWindowLimiter(limit=1, window=10)
    assert limiter.allow("ip", now=0.0) is True
    assert limiter.allow("ip", now=5.0) is False  # encore dans la fenêtre
    assert limiter.allow("ip", now=11.0) is True  # la 1re requête a expiré


def test_cles_independantes():
    limiter = SlidingWindowLimiter(limit=1, window=60)
    assert limiter.allow("a", now=0.0) is True
    assert limiter.allow("b", now=0.0) is True  # autre IP → quota séparé
