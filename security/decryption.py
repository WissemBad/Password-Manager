import base64

from utils import configuration

from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES


class Decryption:
    def __init__(self, instance) -> None:
        self.security = instance


    def CESAR(self, pwd: str, increment: int | None = None) -> str:
        """
        → Déchiffrer avec la méthode de César.
        :param pwd: Le mot de passe ou texte à déchiffrer.
        :param increment: Le nombre de positions à décaler pour chaque caractère (par défaut, utilise la clé de César de l'instance).
        :return: Le texte déchiffré.
        """
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


    def AES(self, encrypted: str, vector: str, salt: str) -> str:
        """
        → Déchiffrer avec la méthode AES.
        :param encrypted: Le texte chiffré en base64 à déchiffrer.
        :param vector: Le vecteur d'initialisation (IV) utilisé pour AES.
        :param salt: Le sel ajouté lors du chiffrement.
        :return: Le texte déchiffré.
        """
        encrypted = base64.b64decode(encrypted.encode('utf-8'))
        cipher = AES.new(self.security.manager.aes_key_load(), AES.MODE_CBC, vector)

        decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)
        decrypted = decrypted.decode('utf-8').removesuffix(salt)
        return decrypted


    @staticmethod
    def RSA(encrypted: int, private_key: tuple[str, str]) -> str | bool:
        """
        → Déchiffrer avec la méthode RSA.
        :param encrypted: Le texte chiffré à déchiffrer sous forme d'entier.
        :param private_key: La clé privée utilisée pour déchiffrer (tuple contenant d et n en base64).
        :return: Le message déchiffré en texte ou False en cas d'erreur.
        """
        d_bytes, n_bytes = base64.b64decode(private_key[0]), base64.b64decode(private_key[1])
        d, n = int.from_bytes(d_bytes, byteorder='big'), int.from_bytes(n_bytes, byteorder='big')

        decrypted = pow(encrypted, d, n)
        decrypted_bytes = decrypted.to_bytes((decrypted.bit_length() + 7) // 8, byteorder='big')

        try: decrypted_message = decrypted_bytes.decode('utf-8')
        except UnicodeDecodeError: return False
        return decrypted_message
