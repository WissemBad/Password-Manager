import base64

from utils import configuration as configuration

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

class Encryption:
    def __init__(self, instance):
        self.security = instance

    def CESAR(self, pwd: str):
        response = ""
        for char in pwd:
            if char in configuration.characters["alphabet"]:
                index = configuration.characters["alphabet"].index(char) + self.security.manager.csr_load_key()
                if not index < len(configuration.characters["alphabet"]): index = index - len(
                    configuration.characters["alphabet"])
                char = configuration.characters["alphabet"][index]
            elif char in configuration.characters["ALPHABET"]:
                index = configuration.characters["ALPHABET"].index(char) + self.security.manager.csr_load_key()
                if not index < len(configuration.characters["ALPHABET"]): index = index - len(
                    configuration.characters["ALPHABET"])
                char = configuration.characters["ALPHABET"][index]
            elif char in configuration.characters["special"]:
                index = configuration.characters["special"].index(char) + self.security.manager.csr_load_key()
                if not index < len(configuration.characters["special"]): index = index - len(
                    configuration.characters["special"])
                char = configuration.characters["special"][index]
            elif char in configuration.characters["numbers"]:
                char = abs(self.security.manager.csr_load_key() + int(char))
            response += str(char)
        return response

    def AES(self, password: str, vector: str):
        salt = get_random_bytes(AES.block_size)
        cipher = AES.new(self.security.manager.aes_load_key(), AES.MODE_CBC, vector)

        encrypted = cipher.encrypt(pad((password + base64.b64encode(salt).decode('utf-8')).encode('utf-8'), AES.block_size))
        return encrypted, base64.b64encode(salt)

    @staticmethod
    def RSA(password: str, public_key):
        e_bytes, n_bytes = base64.b64decode(public_key[0]), base64.b64decode(public_key[1])
        e, n = int.from_bytes(e_bytes, byteorder='big'), int.from_bytes(n_bytes, byteorder='big')

        crypt = int.from_bytes(password.encode('utf-8'), byteorder='big')
        encrypted = pow(crypt, e, n)
        return encrypted


    def custom(self):
        return True

