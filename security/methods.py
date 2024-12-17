import os
import sys
import base64

from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from utils import _config as configuration


# → HACHAGE DES DONNÉES
def hash(pwd: str):
    hashed = sha256(pwd.encode('utf-8')).hexdigest()
    return hashed

# → CHIFFREMENT DES DONNÉES
def encrypt(mode: int, pwd: str, vector: str = None):
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
            if vector is None: raise ValueError("[vector] ne doit pas être vide.")
            pwd = pad(pwd.encode('utf-8'), AES.block_size)
            crypt = AES.new(configuration.keys["AES"], AES.MODE_CBC, vector)

            encrypted = crypt.encrypt(pwd)
            encrypted = base64.b64encode(encrypted).decode('utf-8')

            return encrypted

        # -- CHIFFREMENT : RSA
        case 2:
            return pwd

        # -- CHIFFREMENT : CUSTOM
        case 3:
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

            crypt = AES.new(configuration.keys["AES"], AES.MODE_CBC, vector)
            decrypted = crypt.decrypt(encrypted)

            decrypted = unpad(decrypted, AES.block_size).decode('utf-8')
            return decrypted

        # -- DECRYPTAGE : RSA
        case 2:
            return mode, pwd

        # -- DECRYPTAGE : CUSTOM
        case 3:
            return mode, pwd

# → COMPARAISON DES DONNÉES
def compare(input, stored):
    return input == stored

# Étoiles à la place de la saisie lors de l'input - By ChatGPT
def secure_input(input: str):
    if os.name == 'nt':  # Windows
        import msvcrt
        sys.stdout.write(input)
        sys.stdout.flush()
        password = ""
        while True:
            char = msvcrt.getch()
            if char in {b'\r', b'\n'}:  # Enter key
                break
            elif char == b'\x08':  # Backspace
                if len(password) > 0:
                    password = password[:-1]
                    sys.stdout.write('\b \b')
                    sys.stdout.flush()
            else:
                password += char.decode('utf-8')
                sys.stdout.write("*")
                sys.stdout.flush()
        sys.stdout.write("\n")
        return password
    else:  # Unix/Linux/MacOS
        import termios
        import tty
        sys.stdout.write(input)
        sys.stdout.flush()
        password = ""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                char = sys.stdin.read(1)
                if char == '\n' or char == '\r':  # Gérer Entrée correctement
                    break
                elif char == '\x7f':  # Backspace
                    if len(password) > 0:
                        password = password[:-1]
                        sys.stdout.write('\b \b')  # Supprime une étoile
                        sys.stdout.flush()
                else:
                    password += char
                    sys.stdout.write("*")  # Affiche une étoile
                    sys.stdout.flush()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  # Réinitialise les paramètres
        sys.stdout.write("\n")
        return password