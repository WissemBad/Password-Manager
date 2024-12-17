import os
import base64
import random

from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA

class KeyManager:   
    def __init__(self, instance):
        self.instance = instance

        self.aes_global_key = base64.b64decode(os.getenv("AES_GLOBAL_KEY"))
        self.rsa_public_key = RSA.import_key(base64.b64decode(os.getenv("RSA_PUBLIC_KEY")))
        self.rsa_private_key = RSA.import_key(base64.b64decode(os.getenv("RSA_PRIVATE_KEY")))

        self.aes_directory = "security/keys/encrypted_aes.key"
        self.csr_directory = "security/keys/encrypted_csr.key"

    def double_encrypt(self, key):
        """Chiffrer doublement avec la clé AES et publique RSA."""
        encrypted_key = PKCS1_OAEP.new(self.rsa_public_key).encrypt(key)
        doubly_encrypted_key = AES.new(self.aes_global_key, AES.MODE_ECB).encrypt(pad(encrypted_key, AES.block_size))
        return doubly_encrypted_key

    def double_decrypt(self, doubly_encrypted_key):
        """Déchiffrer doublement avec la clé AES et privée RSA."""
        encrypted_key = unpad(AES.new(self.aes_global_key, AES.MODE_ECB).decrypt(doubly_encrypted_key), AES.block_size)
        key = PKCS1_OAEP.new(self.rsa_private_key).decrypt(encrypted_key)
        return key

    # — Générer une clé secrète AES
    def aes_key_generate(self):
        aes_key = get_random_bytes(32)  # Générer une clé AES de 256 bits
        doubly_encrypted_aes_key = self.double_encrypt(aes_key)

        directory = os.path.dirname(self.aes_directory)
        if not os.path.exists(directory): os.makedirs(directory)
        with open(self.aes_directory, "wb") as key_file: key_file.write(doubly_encrypted_aes_key)
        return aes_key

    # — Charger la clé secrète AES
    def aes_key_load(self):
        if not os.path.exists(self.aes_directory) or os.path.getsize(self.aes_directory) == 0:
            return self.aes_key_generate()

        with open(self.aes_directory, "rb") as key_file:
            doubly_encrypted_aes_key = key_file.read()

        aes_key = self.double_decrypt(doubly_encrypted_aes_key)
        return aes_key

    # — Générer une clé secrète César
    def csr_key_generate(self):
        csr_key = random.randint(0, 25).to_bytes(1, byteorder='big')
        directory = os.path.dirname(self.csr_directory)
        if not os.path.exists(directory): os.makedirs(directory)

        doubly_encrypted_csr_key = self.double_encrypt(csr_key)
        directory = os.path.dirname(self.csr_directory)
        if not os.path.exists(directory): os.makedirs(directory)
        with open(self.csr_directory, "wb") as key_file: key_file.write(doubly_encrypted_csr_key)
        return int.from_bytes(csr_key, byteorder='big') % 26

    # — Charger la clé secrète César
    def csr_key_load(self):
        if not os.path.exists(self.csr_directory) or os.path.getsize(self.csr_directory) == 0:
            return self.csr_key_generate()

        with open(self.aes_directory, "rb") as key_file:
            doubly_encrypted_csr_key = key_file.read()

        csr_key = self.double_decrypt(doubly_encrypted_csr_key)
        return int.from_bytes(csr_key, byteorder='big') % 26
