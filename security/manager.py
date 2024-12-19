import os
import base64
import random
import time

from dotenv import load_dotenv
from utils.methods import console
from utils import configuration

from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA

class KeyManager:
    aes_global_key_size: int = configuration.security["aes_master_key_size"]
    rsa_global_key_size: int = configuration.security["rsa_master_key_size"]

    aes_directory = "security/keys/encrypted_aes.key"
    csr_directory = "security/keys/encrypted_csr.key"

    if os.path.exists('.env'):
        load_dotenv() # Charger les variables d'environnement
        aes_global_key = base64.b64decode(os.getenv("AES_GLOBAL_KEY"))
        rsa_public_key = RSA.import_key(base64.b64decode(os.getenv("RSA_PUBLIC_KEY")))
        rsa_private_key = RSA.import_key(base64.b64decode(os.getenv("RSA_PRIVATE_KEY")))

    def double_encrypt(self, key, user_vector=None):
        """→ Chiffrer doublement avec la clé AES et publique RSA."""
        encrypted_key = PKCS1_OAEP.new(self.rsa_public_key).encrypt(key)
        if user_vector is None: doubly_encrypted_key = AES.new(self.aes_global_key, AES.MODE_ECB).encrypt(pad(encrypted_key, AES.block_size))
        else: doubly_encrypted_key = AES.new(self.aes_global_key, AES.MODE_CBC, user_vector).encrypt(pad(encrypted_key, AES.block_size))
        return doubly_encrypted_key

    def double_decrypt(self, doubly_encrypted_key, user_vector=None):
        """→ Déchiffrer doublement avec la clé AES et privée RSA."""
        if user_vector is None: encrypted_key = unpad(AES.new(self.aes_global_key, AES.MODE_ECB).decrypt(doubly_encrypted_key), AES.block_size)
        else: encrypted_key = unpad(AES.new(self.aes_global_key, AES.MODE_CBC, user_vector).decrypt(doubly_encrypted_key), AES.block_size)
        key = PKCS1_OAEP.new(self.rsa_private_key).decrypt(encrypted_key)
        return key

    def aes_key_generate(self):
        """→ Générer une clé secrète AES et l'enregistrer dans un fichier."""
        aes_key = get_random_bytes(int(self.aes_global_key_size/8))
        doubly_encrypted_aes_key = self.double_encrypt(aes_key)

        directory = os.path.dirname(self.aes_directory)
        if not os.path.exists(directory): os.makedirs(directory)
        with open(self.aes_directory, "wb") as key_file: key_file.write(doubly_encrypted_aes_key)
        return aes_key

    def aes_key_load(self):
        """→ Charger la clé secrète AES."""
        if not os.path.exists(self.aes_directory): return self.aes_key_generate()

        with open(self.aes_directory, "rb") as key_file:
            doubly_encrypted_aes_key = key_file.read()

        return self.double_decrypt(doubly_encrypted_aes_key)

    def csr_key_generate(self):
        """→ Générer une clé secrète César et l'enregistrer dans un fichier."""
        csr_key = random.randint(0, 25).to_bytes(1, byteorder='big')
        directory = os.path.dirname(self.csr_directory)
        if not os.path.exists(directory): os.makedirs(directory)

        doubly_encrypted_csr_key = self.double_encrypt(csr_key)
        directory = os.path.dirname(self.csr_directory)
        if not os.path.exists(directory): os.makedirs(directory)
        with open(self.csr_directory, "wb") as key_file: key_file.write(doubly_encrypted_csr_key)
        return int.from_bytes(csr_key, byteorder='big') % 26

    def csr_key_load(self):
        """→ Charger la clé secrète César."""
        if not os.path.exists(self.csr_directory) or os.path.getsize(self.csr_directory) == 0:
            return self.csr_key_generate()

        with open(self.aes_directory, "rb") as key_file:
            doubly_encrypted_csr_key = key_file.read()

        csr_key = self.double_decrypt(doubly_encrypted_csr_key)
        return int.from_bytes(csr_key, byteorder='big') % 26

    def initialize_security(self):
        """→ Initialiser les clés RSA et AES pour l'application."""
        console("yellow", "[🛈] Info : Initialisation des clés RSA et AES pour l'application...")
        aes_key = get_random_bytes(int(self.aes_global_key_size/8))
        rsa_key = RSA.generate(self.rsa_global_key_size)

        private_key = rsa_key.export_key()
        public_key = rsa_key.publickey().export_key()

        aes_key_b64 = base64.b64encode(aes_key).decode('utf-8')
        private_key_b64 = base64.b64encode(private_key).decode('utf-8')
        public_key_b64 = base64.b64encode(public_key).decode('utf-8')

        with open('.env', 'w') as env_file:
            env_file.write(f"AES_GLOBAL_KEY={aes_key_b64}\n")
            env_file.write(f"RSA_PUBLIC_KEY={public_key_b64}\n")
            env_file.write(f"RSA_PRIVATE_KEY={private_key_b64}\n")
        console("green", "Les clés RSA et AES ont été générées avec succès."), load_dotenv()

        self.aes_global_key = base64.b64decode(os.getenv("AES_GLOBAL_KEY"))
        self.rsa_public_key = RSA.import_key(base64.b64decode(os.getenv("RSA_PUBLIC_KEY")))
        self.rsa_private_key = RSA.import_key(base64.b64decode(os.getenv("RSA_PRIVATE_KEY")))
        return time.sleep(1.5), True
