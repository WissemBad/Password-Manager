from argon2 import PasswordHasher

class Hasher:
    hasher = PasswordHasher()


    def hash(self, password: str) -> str:
        """
        → Hacher un mot de passe grâce à Argon2.
        :param password: Le mot de passe à hacher.
        :return: Le mot de passe haché.
        """
        return self.hasher.hash(password)


    def verify(self, hashed_password: str, password: str) -> bool:
        """
        → Vérifier un mot de passe haché grâce à Argon2.
        :param hashed_password: Le mot de passe haché à vérifier.
        :param password: Le mot de passe à comparer avec le mot de passe haché.
        :return: True si le mot de passe est correct, False sinon.
        """
        try: self.hasher.verify(hashed_password, password); return True
        except Exception: return False
