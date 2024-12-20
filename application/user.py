from utils import methods
from utils import configuration


class User:
    def __init__(self, username: str, password: str, app):
        self.app = app
        self.database = app.database

        self.username = username
        self.password = self.app.security.hasher.hash(password)

        self.exists = self.database.user.exists(self.username)
        self.id:int = self.get_id()

        self.aes_encryption_key = self.app.security.get_aes_vector(password)
        self.rsa_public_key = None
        self.rsa_private_key = None
        self.safety_auth = False

    def init_dependencies(self):
        """→ Initialiser les dépendances de l'utilisateur."""
        self.rsa_public_key, self.rsa_private_key = self.database.user.get_encryption_keys(self.id)

    def get_id(self):
        """→ Récupérer l'identifiant de l'utilisateur"""
        return self.database.user.get_by_name(self.username)["id"] if self.exists \
        else methods.auto_increment(self.database.complete["utilisateur"])

    def register(self):
        """→ Enregistrer un nouveau compte utilisateur."""
        methods.console("blue", "[ί] Création de clé de chiffrement personnelle...")
        self.rsa_public_key, self.rsa_private_key = self.app.security.generate_rsa_keys(configuration.security["rsa_standard_key_size"], self.aes_encryption_key)
        return self.database.user.create(self)

    def delete(self):
        """→ Suppression de compte utilisateur."""
        if not methods.confirm("supprimer définitivement votre compte"): return False
        return self.database.user.delete(self.id)

    def login(self, password: str):
        """→ Connexion de l'utilisateur."""
        if not self.exists: return False
        head = self.database.user.get_by_name(self.username)

        if not head["id"] == self.id: return False
        return self.app.security.hasher.verify(head["password"], password)


    def logout(self):
        """→ Déconnexion de l'utilisateur"""
        if not self.app.logged_in or self.app.user != self: return False
        return True


