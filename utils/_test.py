import os
from application.main import Application
from application.user import User

import math
import base64

from security.hash import Hasher
from security.manager import KeyManager
from security.encryption import Encryption
from security.decryption import Decryption
from utils.methods import generate_prime

from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES

import os
from application.main import Application
from application.user import User

Application = Application()

def get_aes_vector(password: str):
    """→ Obtenir un vecteur dérivé du mot de passe pour le chiffrement AES."""
    derived = PBKDF2(password, b'', count=1000000)
    return derived[:AES.block_size]

if __name__ == "__main__":
    # Vérifie si .env existe
    if not os.path.exists(".env"): Application.security.manager.initialize_security()

    # Lancer l'application
    Application.user = User("wissem", "Wissem", Application)
    Application.after_connect()

    # Application.init_dependencies()
    # print(Application.security.encrypt.AES("Wissem", get_aes_vector("Wissem")))