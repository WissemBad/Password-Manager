from argon2 import PasswordHasher

class Hasher:
    def __init__(self, instance):
        self.instance = instance
        self.hasher = PasswordHasher()

    # - Hachage d'un mot de passe avec Argon2
    def hash(self, password: str) -> str:
        return self.hasher.hash(password)

    # - Vérification d'un mot de passe avec Argon2
    def verify(self, hashed_password: str, password: str ) -> bool:
        try:
            self.hasher.verify(hashed_password, password)
            return True
        except Exception: return False

