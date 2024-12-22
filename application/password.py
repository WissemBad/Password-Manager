import base64
import random

from application.main import Application

from utils import methods
from utils import configuration


class Password:
    def __init__(self, crypt: bool, password: str, encryption_type: str, app: Application, encryption_key: str = None) -> None:
        self.app: Application = app

        if crypt:
            self.encryption_type: str = encryption_type
            self.encrypted, self.encryption_key = self.encrypt(password)
            self.strength: int = get_strength(password)
            self.csr_key = encryption_key
        else:
            self.encrypted: str = password
            self.encryption_key: str = encryption_key
            self.encryption_type: str = encryption_type

            match self.encryption_type:
                case "AES": self.encryption_key_formatted = encryption_key
                case "CESAR": self.encryption_key_formatted = encryption_key
                case "RSA": self.encryption_key_formatted = [
                            base64.b64encode(self.app.security.manager.double_decrypt(base64.b64decode(encryption_key[0].encode("utf-8")), self.app.user.aes_encryption_key)),
                            base64.b64encode(self.app.security.manager.double_decrypt(base64.b64decode(encryption_key[1].encode("utf-8")), self.app.user.aes_encryption_key))
                        ]

            self.decrypted = self.decrypt(password)
            self.strength = get_strength(self.decrypted)


    def encrypt(self, password: str) -> tuple[str, str | None]:
        """
        → Chiffre le mot de passe avec le type de cryptage spécifié.
        :param password: Le mot de passe brut.
        :return: Le mot de passe chiffré et la clé de chiffrement associée.
        """
        try:
            match self.encryption_type:
                case "AES": return self.app.security.encrypt.AES(password, self.app.user.aes_encryption_key)
                case "RSA": return self.app.security.encrypt.RSA(password, self.app.user.rsa_public_key), None
                case "CESAR": return self.app.security.encrypt.CESAR(password, self.csr_key), self.csr_key
        except Exception as error:
            methods.console("red", f"[✘] Erreur : Impossible de chiffrer le mot de passe. Vérifiez votre compte ou contactez le support.\n{error}")
            return "", None

    def decrypt(self, password: str) -> str:
        """
        → Déchiffre le mot de passe avec le type de cryptage spécifié.
        :param password: Le mot de passe chiffré.
        :return: Le mot de passe déchiffré.
        """
        try:
            match self.encryption_type:
                case "AES": return self.app.security.decrypt.AES(password, self.app.user.aes_encryption_key, self.encryption_key_formatted)
                case "RSA": return self.app.security.decrypt.RSA(password, self.encryption_key_formatted)
                case "CESAR": return self.app.security.decrypt.CESAR(password, self.encryption_key_formatted)
        except Exception as error:
            methods.console("red", f"[✘] Erreur : Impossible de déchiffrer le mot de passe. Vérifiez votre compte ou contactez le support.\n{error}")
            return ""


def get_strength(password: str) -> int:
    """
    → Évalue la robustesse d'un mot de passe.
    :param password: Le mot de passe à évaluer.
    :return: Un entier représentant la robustesse du mot de passe (1 à 4).
    """
    strength = 0
    numbers = sum(char.isdigit() for char in password)
    specials = sum(char in configuration.characters["special"] for char in password)
    length = len(password)

    if not password.islower() and not password.isupper(): strength += 1  # Ne contient pas que des lettres majuscules ou minuscules.
    if length >= 8: strength += 1  # Au moins 8 caractères.
    if numbers >= 2: strength += 1  # Au moins 2 chiffres.
    if specials >= 1: strength += 1  # Au moins 1 caractère spécial.

    return max(strength, 1)


def generate_password(
    length: int = 12,
    use_mixed_case: bool = True,
    use_numbers: bool = True,
    use_specials: bool = True,
    use_dictionary: bool = False,
    strength: int = 3
) -> tuple[bool, str | None]:
    """
    → Génère un mot de passe aléatoire en fonction des critères donnés.
    :param length: Longueur du mot de passe.
    :param use_mixed_case: Inclure des majuscules et minuscules.
    :param use_numbers: Inclure des chiffres.
    :param use_specials: Inclure des caractères spéciaux.
    :param use_dictionary: Utiliser un mot du dictionnaire.
    :param strength: Robustesse souhaitée (1 à 4).
    :return: Un tuple contenant un booléen de succès et le mot de passe ou un message d'erreur.
    """
    character_pool = configuration.characters["alphabet"]
    password = ""

    if use_mixed_case: character_pool += configuration.characters["ALPHABET"]
    if use_numbers: character_pool += configuration.characters["numbers"]
    if use_specials: character_pool += configuration.characters["special"]
    if not character_pool: return False, "Impossible de générer un mot de passe sans caractères."

    if use_dictionary: password = methods.get_random_word(length)
    else:
        password = "".join(random.choice(character_pool) for _ in range(length))
        if use_mixed_case: password = methods.get_random_caps(password)

    if strength == 1: return True, password
    if strength == 4 and not (use_numbers and use_specials and use_mixed_case and length >= 8): return False, "Impossible de générer un mot de passe avec la robustesse souhaitée."

    for _ in range(50):
        if get_strength(password) >= strength: break
        if use_numbers: password += random.choice(configuration.characters["numbers"])
        if use_specials: password += random.choice(configuration.characters["special"])
    else:
        return False, "Impossible de générer un mot de passe avec la robustesse souhaitée."
    return True, password
