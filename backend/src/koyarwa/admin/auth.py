from __future__ import annotations

import time

from starlette.requests import Request
from starlette.responses import RedirectResponse

#: Clé sous laquelle l'utilisateur admin est stocké dans la session.
SESSION_KEY = "admin_user"


class RequiresLogin(Exception):
    """Levée quand une page admin protégée est demandée sans session valide."""


def require_admin(request: Request) -> str:
    """Dépendance FastAPI : renvoie l'utilisateur en session, sinon exige un login."""
    user = request.session.get(SESSION_KEY)
    if not user:
        raise RequiresLogin
    return user


class LoginThrottle:
    """Verrou anti-force-brute : après trop d'échecs pour un identifiant, les
    tentatives sont refusées pendant une fenêtre de refroidissement.

    En mémoire du process (défense en profondeur mono-instance ; se réinitialise
    au redémarrage). Clé par identifiant : borne les essais sur un compte donné.
    """

    def __init__(self, *, max_failures: int = 5, lockout_seconds: float = 900) -> None:
        self._max = max_failures
        self._lockout = lockout_seconds
        self._failures: dict[str, tuple[int, float]] = {}  # clé -> (nb, dernier_échec)

    @staticmethod
    def _key(username: str) -> str:
        return username.strip().lower()

    def locked_for(self, username: str, now: float | None = None) -> float:
        """Secondes de verrou restantes (0.0 si le compte n'est pas verrouillé)."""
        now = time.monotonic() if now is None else now
        count, last = self._failures.get(self._key(username), (0, 0.0))
        if count < self._max:
            return 0.0
        return max(0.0, self._lockout - (now - last))

    def record_failure(self, username: str, now: float | None = None) -> None:
        now = time.monotonic() if now is None else now
        key = self._key(username)
        count, last = self._failures.get(key, (0, 0.0))
        # Le verrou expiré repart de zéro.
        if count >= self._max and (now - last) >= self._lockout:
            count = 0
        self._failures[key] = (count + 1, now)

    def reset(self, username: str | None = None) -> None:
        """Oublie les échecs d'un identifiant (après succès), ou de tous."""
        if username is None:
            self._failures.clear()
        else:
            self._failures.pop(self._key(username), None)


#: Verrou partagé par le process (câblé dans le routeur de connexion).
login_throttle = LoginThrottle()


async def requires_login_handler(request: Request, exc: RequiresLogin) -> RedirectResponse:
    """Handler d'exception : redirige les accès non authentifiés vers le login."""
    return RedirectResponse("/admin/login", status_code=303)
