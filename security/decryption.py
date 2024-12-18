import base64
from utils import _config as configuration

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

class Decryption:
    def __init__(self, instance):
        self.security = instance

    def CESAR(self, pwd: str):
        response = ""
        for char in pwd:
            if char in configuration.characters["alphabet"]:
                index = configuration.characters["alphabet"].index(char) - self.security.manager.csr_load_key()
                if not index >= 0: index = len(configuration.characters["alphabet"]) + index
                char = configuration.characters["alphabet"][index]
            elif char in configuration.characters["ALPHABET"]:
                index = configuration.characters["ALPHABET"].index(char) - self.security.manager.csr_load_key()
                if not index >= 0: index = len(configuration.characters["ALPHABET"]) + index
                char = configuration.characters["ALPHABET"][index]
            elif char in configuration.characters["special"]:
                index = configuration.characters["special"].index(char) - self.security.manager.csr_load_key()
                if not index >= 0: index = len(configuration.characters["special"]) + index
                char = configuration.characters["special"][index]
            elif char in configuration.characters["numbers"]:
                char = abs(int(char) - self.security.manager.csr_load_key())
            response += str(char)
        return response

    def AES(self, encrypted: bytes, vector: str, salt: str):
        salt = base64.b64decode(salt)
        cipher = AES.new(self.security.manager.aes_load_key(), AES.MODE_CBC, vector)

        decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)
        decrypted = decrypted.decode('utf-8').removesuffix(salt.decode('utf-8'))
        return decrypted

    @staticmethod
    def RSA(encrypted: int, private_key):
        d_bytes, n_bytes = base64.b64decode(private_key[0]), base64.b64decode(private_key[1])
        d, n = int.from_bytes(d_bytes, byteorder='big'), int.from_bytes(n_bytes, byteorder='big')

        decrypted = pow(encrypted, d, n)
        decrypted_bytes = decrypted.to_bytes((decrypted.bit_length() + 7) // 8, byteorder='big')

        try: decrypted_message = decrypted_bytes.decode('utf-8')
        except UnicodeDecodeError: return False
        return decrypted_message

    def custom(self):
        return True

