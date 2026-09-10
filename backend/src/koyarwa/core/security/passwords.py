"""Hachage et vérification des mots de passe.

Argon2 par défaut (repli bcrypt selon ce qui est installé). L'application ne
manipule jamais de mot de passe en clair au repos.
"""

from pwdlib import PasswordHash

_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return _hasher.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return _hasher.verify(password, hashed)
