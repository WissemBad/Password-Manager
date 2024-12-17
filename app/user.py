from utils import methods
from security import methods as security

class User(object):
    def __init__(self, username: str, password: str, app):
        self.app = app
        self.database = app.database

        self.username = username
        self.password = security.hash(password)

        self.exists = self.get_exists()
        self.id:int = self.get_id()

    # → Récupérer le statut de l'utilisateur
    def get_exists(self):
        return self.database.user.exists(self.username)

    # → Récupérer l'identifiant de l'utilisateur
    def get_id(self):
        return self.database.user.get_by_name(self.username)["id"] if self.exists \
            else methods.auto_increment(self.database["utilisateur"])

    # → Ajouter un utilisateur à la base de données
    def register(self):
        if self.exists: return False
        user = {"id": self.id, "username": self.username, "password": self.password}
        return self.database.user.create(user)

    # → Supprimer un utilisateur de la base de données
    def delete(self):
        if not self.exists: return False
        if not methods.confirm("supprimer définitivement votre compte"): return False
        return self.database.user.delete(self.id)

    # → Connexion à l'application
    def login(self):
        if not self.exists: return False
        head = self.database.user.get_by_name(self.username)

        if not head["id"] == self.id: return False
        return security.compare(head["password"], self.password)

    # → Déconnexion de l'application
    def logout(self):
        if not self.app.logged_in or self.app.user != self: return False
        return True


