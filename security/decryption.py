import base64
from utils import configuration as configuration

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

class Decryption:
    def __init__(self, instance):
        self.security = instance

    def CESAR(self, pwd: str, increment: int or None = None):
        """→ Déchiffrer avec la méthode de César."""
        response = ""
        if increment is None: increment = self.security.manager.csr_key_load()

        for char in pwd:
            if char in configuration.characters["alphabet"]:
                index = (configuration.characters["alphabet"].index(char) - increment) % len(configuration.characters["alphabet"])
                char = configuration.characters["alphabet"][index]
            elif char in configuration.characters["ALPHABET"]:
                index = (configuration.characters["ALPHABET"].index(char) - increment) % len(configuration.characters["ALPHABET"])
                char = configuration.characters["ALPHABET"][index]
            elif char in configuration.characters["special"]:
                index = (configuration.characters["special"].index(char) - increment) % len(configuration.characters["special"])
                char = configuration.characters["special"][index]
            elif char in configuration.characters["numbers"]:
                index = (configuration.characters["special"].index(char) - increment) % len(configuration.characters["numbers"])
                char = configuration.characters["special"][index]
            response += str(char)
        return response

    def AES(self, encrypted: str, vector: str, salt: str):
        """→ Déchiffrer avec la méthode AES."""
        salt = base64.b64decode(salt.encode('utf-8'))
        encrypted = base64.b64decode(encrypted.encode('utf-8'))
        cipher = AES.new(self.security.manager.aes_key_load(), AES.MODE_CBC, vector)

        decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)
        decrypted = decrypted.decode('utf-8').removesuffix(salt.decode('utf-8'))
        return decrypted

    @staticmethod
    def RSA(encrypted: int, private_key):
        """→ Déchiffrer avec la méthode RSA."""
        d_bytes, n_bytes = base64.b64decode(private_key[0]), base64.b64decode(private_key[1])
        d, n = int.from_bytes(d_bytes, byteorder='big'), int.from_bytes(n_bytes, byteorder='big')

        decrypted = pow(encrypted, d, n)
        decrypted_bytes = decrypted.to_bytes((decrypted.bit_length() + 7) // 8, byteorder='big')

        try: decrypted_message = decrypted_bytes.decode('utf-8')
        except UnicodeDecodeError: return False
        return decrypted_message

    @staticmethod
    def custom():
        """→ Déchiffrer avec une méthode personnalisée."""
        return True

