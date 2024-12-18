from utils import configuration as configuration

class Password:
    def __init__(self, password, encryption_type, app):
        self.app = app
        self.strength:int = self.get_strength(password)
        self.encryption_type:str = encryption_type
        self.encrypted, self.encryption_key = self.encrypt(password)

    def encrypt(self, password):
        match self.encryption_type:
            case "AES":
                return self.app.security.encrypt.AES(password, self.app.user.aes_encryption_key)
            case "RSA":
                return self.app.security.encrypt.RSA(password, self.app.user.rsa_public_key), None
            case "CESAR":
                return self.app.security.encrypt.CESAR(password), None
            case _: return None, None

    @staticmethod
    def get_strength(password):
        strength = 1
        numbers = 0
        specials = 0
        length = len(password)

        for char in password:
            if char.isdigit(): numbers += 1
            if char in configuration.characters["special"]: specials += 1

        if not password.islower() and not password.isupper(): strength += 1  # - Ne contient pas que des lettres majuscules ou minuscules.
        if length > 8: strength += 1    # - Au moins 8 caractères
        if numbers >= 2: strength += 1  # - Au moins 2 chiffres
        if specials > 0: strength += 1  # - Au moins 1 caractère spécial

        return strength
