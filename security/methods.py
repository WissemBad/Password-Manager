import base64

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

from app import _config as configuration

# → CHIFFREMENT DES DONNÉES
def encrypt(mode: int, pwd: str):
    match mode:

        # -- CHIFFREMENT : CESAR
        case 0:
            response = ""
            for char in pwd:
                if char in configuration.characters["alphabet"]:
                    index = configuration.characters["alphabet"].index(char) + configuration.keys["CESAR"]
                    if not index < len(configuration.characters["alphabet"]): index = index - len(configuration.characters["alphabet"])
                    char = configuration.characters["alphabet"][index]
                elif char in configuration.characters["ALPHABET"]:
                    index = configuration.characters["ALPHABET"].index(char) + configuration.keys["CESAR"]
                    if not index < len(configuration.characters["ALPHABET"]): index = index - len(configuration.characters["ALPHABET"])
                    char = configuration.characters["ALPHABET"][index]
                elif char in configuration.characters["special"]:
                    index = configuration.characters["special"].index(char) + configuration.keys["CESAR"]
                    if not index < len(configuration.characters["special"]): index = index - len(configuration.characters["special"])
                    char = configuration.characters["special"][index]
                elif char.isnumeric():
                    char = abs(configuration.keys["CESAR"] + int(char))
                response += str(char)
            return response

        # -- CHIFFREMENT : AES
        case 1:
            pwd = pad(pwd.encode('utf-8'), AES.block_size)
            vector = get_random_bytes(16)

            crypt = AES.new(configuration.keys["AES"], AES.MODE_CBC, vector)
            encrypted = crypt.encrypt(pwd)

            encrypted = base64.b64encode(encrypted).decode('utf-8')
            vector = base64.b64encode(vector).decode('utf-8')

            return encrypted, vector

        # -- CHIFFREMENT : CUSTOM
        case 2:
            return pwd

# → DÉCHIFFREMENT DES DONNÉES
def decrypt(mode: int, pwd: str, vector: str = None):
    match mode:

        # -- DECRYPTAGE : CESAR
        case 0:
            response = ""
            for char in pwd:
                if char in configuration.characters["alphabet"]:
                    index = configuration.characters["alphabet"].index(char) - configuration.keys["CESAR"]
                    if not index >= 0: index = len(configuration.characters["alphabet"]) + index
                    char = configuration.characters["alphabet"][index]
                elif char in configuration.characters["ALPHABET"]:
                    index = configuration.characters["ALPHABET"].index(char) - configuration.keys["CESAR"]
                    if not index >= 0: index = len(configuration.characters["ALPHABET"]) + index
                    char = configuration.characters["ALPHABET"][index]
                elif char in configuration.characters["special"]:
                    index = configuration.characters["special"].index(char) - configuration.keys["CESAR"]
                    if not index >= 0: index = len(configuration.characters["special"]) + index
                    char = configuration.characters["special"][index]
                elif char.isnumeric():
                    char = abs(int(char) - configuration.keys["CESAR"])
                response += str(char)
            return response

        # -- DECRYPTAGE : AES
        case 1:
            if vector is None: raise ValueError("[vector] ne doit pas être vide.")
            encrypted = base64.b64decode(pwd)
            vector = base64.b64decode(vector)

            crypt = AES.new(configuration.keys["AES"], AES.MODE_CBC, vector)
            decrypted = crypt.decrypt(encrypted)

            decrypted = unpad(decrypted, AES.block_size).decode('utf-8')
            return decrypted

        # -- DECRYPTAGE : CUSTOM
        case 2:
            return mode, pwd

def compare(input, vector1, stored, vector2):
    input = decrypt(1, input, vector1)
    stored = decrypt(1, stored, vector2)
    return input == stored

# VECTOR = USER ACCOUNT PASSWORD