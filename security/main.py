import math
import base64

from utils.methods import generate_prime

from security.hash import Hasher
from security.manager import KeyManager
from security.encryption import Encryption
from security.decryption import Decryption

from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES


class Security:
    def __init__(self, app):
        self.app = app
        self.manager = KeyManager()

        self.hasher = Hasher()
        self.encrypt = None
        self.decrypt = None


    def init_dependencies(self):
        """ → Initialiser les dépendances de sécurité."""
        self.encrypt = Encryption(self)
        self.decrypt = Decryption(self)


    @staticmethod
    def get_aes_vector(password: str) -> bytes:
        """
        → Obtenir un vecteur dérivé du mot de passe pour le chiffrement AES.
        :param password: Le mot de passe à utiliser pour dériver le vecteur.
        :return: Un vecteur d'initialisation (IV) de taille AES.block_size.
        """
        derived = PBKDF2(password, b'', count=1000000)
        return derived[:AES.block_size]


    def generate_rsa_keys(self, key_size: int, user_vector: bytes) -> tuple[list[str], list[str]]:
        """
        → Générer une paire de clés RSA.
        :param key_size: La taille de la clé RSA en bits.
        :param user_vector: Le vecteur utilisé pour l'encryptage des clés privées.
        :return: Un tuple contenant la clé publique (list de deux chaînes) et la clé privée (list de deux chaînes).
        """
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

        e_bytes = e.to_bytes((e.bit_length() + 7) // 8, byteorder='big')
        n_bytes = n.to_bytes((n.bit_length() + 7) // 8, byteorder='big')
        d_bytes = d.to_bytes((d.bit_length() + 7) // 8, byteorder='big')

        private_encryption = [self.manager.double_encrypt(d_bytes, user_vector), self.manager.double_encrypt(n_bytes, user_vector)]

        public_key = [base64.b64encode(e_bytes).decode('utf-8'), base64.b64encode(n_bytes).decode('utf-8')]
        private_key = [base64.b64encode(private_encryption[0]).decode('utf-8'), base64.b64encode(private_encryption[1]).decode('utf-8')]
        return public_key, private_key