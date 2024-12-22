from utils import configuration
from utils import methods


class User:
    def __init__(self, username: str, password: str, app) -> None:
        self.app = app
        self.database = app.database

        self.username: str = username
        self.password: str = self.app.security.hasher.hash(password)

        self.exists: bool = self.database.user.exists(self.username)
        self.id: int = self.get_id()

        self.aes_encryption_key: bytes = self.app.security.get_aes_vector(password)
        self.rsa_public_key: str | None = None
        self.rsa_private_key: str | None = None
        self.safety_auth: bool = False


    def init_dependencies(self) -> None:
        """ → Initialiser les dépendances de l'utilisateur."""
        self.rsa_public_key, self.rsa_private_key = self.database.user.get_encryption_keys(self.id)


    def get_id(self) -> int:
        """
        → Récupérer l'identifiant de l'utilisateur.
        :return: L'identifiant de l'utilisateur s'il existe, sinon un nouvel ID incrémenté.
        """
        return self.database.user.get_by_name(self.username)["id"] if self.exists \
            else methods.auto_increment(self.database.complete["utilisateur"])


    def register(self) -> bool:
        """
        → Enregistrer un nouveau compte utilisateur.
        :return: True si l'enregistrement a réussi, False sinon.
        """
        if self.exists: return False
        methods.console("blue", "[ί] Création de clé de chiffrement personnelle...")
        self.rsa_public_key, self.rsa_private_key = self.app.security.generate_rsa_keys(configuration.security["rsa_standard_key_size"], self.aes_encryption_key)
        return self.database.user.create(self)


    def delete(self) -> bool:
        """
        → Supprimer le compte utilisateur.
        :return: True si la suppression a réussi, False sinon.
        """
        if not methods.confirm("supprimer définitivement votre compte"): return False
        return self.database.user.delete(self.id)


    def login(self, password: str) -> bool:
        """
        → Connecter l'utilisateur.
        :param password: Le mot de passe fourni par l'utilisateur.
        :return: True si la connexion a réussi, False sinon.
        """
        if not self.exists:
            return False
        head = self.database.user.get_by_name(self.username)

        if head["id"] != self.id:
            return False
        return self.app.security.hasher.verify(head["password"], password)


    def logout(self) -> bool:
        """
        → Déconnecter l'utilisateur.
        :return: True si la déconnexion a réussi, False sinon.
        """
        if not self.app.logged_in or self.app.user != self:
            return False
        return True
