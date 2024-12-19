from argon2 import PasswordHasher

class Hasher:
    hasher = PasswordHasher()

    def hash(self, password: str) -> str:
        """→ Hacher un mot de passe grâce à Argon2."""
        return self.hasher.hash(password)

    def verify(self, hashed_password: str, password: str ) -> bool:
        """→ Vérifier un mot de passe haché grâce à Argon2."""
        try:
            self.hasher.verify(hashed_password, password)
            return True
        except Exception: return False