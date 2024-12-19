import base64

from utils import configuration as configuration

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

class Encryption:
    def __init__(self, instance):
        self.security = instance

    def CESAR(self, pwd: str, increment: int or None = None):
        """→ Chiffrer avec la méthode de César."""
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

    def AES(self, password: str, vector: str):
        """→ Chiffrer avec la méthode AES."""
        if len(vector) != AES.block_size:
            raise ValueError("Le vecteur d'initialisation (IV) doit avoir une longueur de {} octets.".format(AES.block_size))

        salt = get_random_bytes(AES.block_size)
        key = self.security.manager.aes_key_load()

        if len(key) not in {16, 24, 32}:
            raise ValueError("La clé AES doit avoir une longueur de 16, 24 ou 32 octets.")

        cipher = AES.new(key, AES.MODE_CBC, vector)
        padded_data = pad((password + base64.b64encode(salt).decode('utf-8')).encode('utf-8'), AES.block_size)
        encrypted = base64.b64encode(cipher.encrypt(padded_data)).decode('utf-8')

        return encrypted, base64.b64encode(salt).decode('utf-8')

    @staticmethod
    def RSA(password: str, public_key):
        """→ Chiffrer avec la méthode RSA."""
        e_bytes, n_bytes = base64.b64decode(public_key[0]), base64.b64decode(public_key[1])
        e, n = int.from_bytes(e_bytes, byteorder='big'), int.from_bytes(n_bytes, byteorder='big')

        crypt = int.from_bytes(password.encode('utf-8'), byteorder='big')
        encrypted = pow(crypt, e, n)
        return encrypted

    @staticmethod
    def custom():
        """→ Chiffrer avec une méthode personnalisée."""
        return True

