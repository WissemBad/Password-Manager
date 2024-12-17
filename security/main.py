import math
import base64

from security.hash import Hasher
from security.manager import KeyManager
from security.encryption import Encryption
from security.decryption import Decryption
from utils.methods import generate_prime

from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES


class Security:
    def __init__(self, app):
        self.app = app
        self.manager = KeyManager(self)

        self.hasher = Hasher(self)
        self.encrypt = Encryption(self)
        self.decrypt = Decryption(self)

    @staticmethod # Générer un vecteur d'initialisation dérivée du mot de passe.
    def get_aes_vector(password: str):
        derived = PBKDF2(password, b'', count=1000000)
        return derived[:AES.block_size]

    # Générer des clés de chiffrement RSA publique et privée.
    def generate_rsa_keys(self, key_size):
        bits = key_size // 2
        p = generate_prime(bits)
        q = generate_prime(bits)
        while p == q:
            q = generate_prime(bits)

        n = p * q
        phi = (p - 1) * (q - 1)

        e = 65537 if math.gcd(65537, phi) == 1 else 3
        while math.gcd(e, phi) != 1:
            e += 2
        d = pow(e, -1, phi)

        # Clé publique et privée
        e_bytes = e.to_bytes((e.bit_length() + 7) // 8, byteorder='big')
        n_bytes = n.to_bytes((n.bit_length() + 7) // 8, byteorder='big')
        d_bytes = d.to_bytes((d.bit_length() + 7) // 8, byteorder='big')

        private_encryption = [self.manager.double_encrypt(d_bytes), self.manager.double_encrypt(n_bytes)]

        public_key = [base64.b64encode(e_bytes).decode('utf-8'), base64.b64encode(n_bytes).decode('utf-8')]
        private_key = [base64.b64encode(private_encryption[0]).decode('utf-8'), base64.b64encode(private_encryption[1]).decode('utf-8')]

        return public_key, private_key






