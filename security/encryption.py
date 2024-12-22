import base64

from utils import configuration
from security.main import Security

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

class Encryption:
    def __init__(self, instance: Security) -> None:
        self.security: Security = instance


    def CESAR(self, pwd: str, increment: int | None = None) -> str:
        """
        → Chiffrer avec la méthode de César.
        :param pwd: Le mot de passe ou texte à chiffrer.
        :param increment: Le nombre de positions à décaler pour chaque caractère (par défaut, utilise la clé de César de l'instance).
        :return: Le texte chiffré.
        """
        response = ""
        if increment is None: increment = self.security.manager.csr_key_load()
        for char in pwd:
            if char in configuration.characters["alphabet"]:
                index = (configuration.characters["alphabet"].index(char) + increment) % len(configuration.characters["alphabet"])
                char = configuration.characters["alphabet"][index]
            elif char in configuration.characters["ALPHABET"]:
                index = (configuration.characters["ALPHABET"].index(char) + increment) % len(configuration.characters["ALPHABET"])
                char = configuration.characters["ALPHABET"][index]
            elif char in configuration.characters["special"]:
                index = (configuration.characters["special"].index(char) + increment) % len(configuration.characters["special"])
                char = configuration.characters["special"][index]
            elif char in configuration.characters["numbers"]:
                index = (configuration.characters["special"].index(char) + increment) % len(configuration.characters["numbers"])
                char = configuration.characters["special"][index]
            response += str(char)
        return response


    def AES(self, password: str, vector: str) -> tuple[str, str]:
        """
        → Chiffrer avec la méthode AES.
        :param password: Le mot de passe à chiffrer.
        :param vector: Le vecteur d'initialisation (IV) pour AES.
        :return: Un tuple contenant le texte chiffré et le sel utilisé.
        """
        salt = get_random_bytes(AES.block_size)
        key = self.security.manager.aes_key_load()
        cipher = AES.new(key, AES.MODE_CBC, vector)

        padded_data = pad((password + base64.b64encode(salt).decode('utf-8')).encode('utf-8'), AES.block_size)
        encrypted = base64.b64encode(cipher.encrypt(padded_data)).decode('utf-8')
        return encrypted, base64.b64encode(salt).decode('utf-8')


    @staticmethod
    def RSA(password: str, public_key: tuple[str, str]) -> int:
        """
        → Chiffrer avec la méthode RSA.
        :param password: Le mot de passe à chiffrer.
        :param public_key: La clé publique sous forme d'un tuple contenant (e, n) en base64.
        :return: Le texte chiffré sous forme d'entier.
        """
        e_bytes, n_bytes = base64.b64decode(public_key[0]), base64.b64decode(public_key[1])
        e, n = int.from_bytes(e_bytes, byteorder='big'), int.from_bytes(n_bytes, byteorder='big')

        crypt = int.from_bytes(password.encode('utf-8'), byteorder='big')
        encrypted = pow(crypt, e, n)
        return encrypted
