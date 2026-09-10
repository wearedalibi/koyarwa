from starlette.requests import Request

from koyarwa.api.ratelimit import RateLimitMiddleware


def _request(headers: dict[str, str], client_host: str) -> Request:
    scope = {
        "type": "http",
        "headers": [(k.lower().encode(), v.encode()) for k, v in headers.items()],
        "client": (client_host, 12345),
    }
    return Request(scope)


def _mw(*, trust_proxy: bool) -> RateLimitMiddleware:
    return RateLimitMiddleware(
        lambda scope, receive, send: None,
        limit=1,
        window_seconds=60,
        trust_proxy=trust_proxy,
    )


def test_cle_derivee_de_xff_quand_proxy_de_confiance():
    mw = _mw(trust_proxy=True)
    # Le client a pu injecter "1.1.1.1" ; nginx ajoute l'IP réelle en dernier.
    req = _request({"x-forwarded-for": "1.1.1.1, 203.0.113.7"}, "10.0.0.1")
    assert mw._client_key(req) == "203.0.113.7"


def test_cle_ignore_xff_sans_proxy_de_confiance():
    mw = _mw(trust_proxy=False)
    req = _request({"x-forwarded-for": "1.1.1.1"}, "10.0.0.1")
    assert mw._client_key(req) == "10.0.0.1"
