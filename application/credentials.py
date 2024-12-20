from application.user import User
from application.password import Password

class Credentials:
    def __init__(self, app, id: int, website: str = None, login: str = None, password: str = None, encryption_type: str = None, encryption_key: str = None, labels: list = None):
        self.app = app
        self.database = self.app.database

        self.id:int = id
        self.exists = self.database.credentials.exists(self.id)

        if self.exists:
            self.data = self.database.credentials.get_by_id(self.id)
            self.website = self.data["website"]
            self.login = self.data["login"]
            self.labels = self.data["labels"]
            self.password_encrypted = Password(self.data["password"], self.data["encryption_type"], self.app, self.data["encryption_key"])
            self.password_history = self.data["history"]
            self.user_id = self.data["user_id"]
        elif website and login and password and encryption_type:
            self.website:str = website
            self.login:str = login
            self.password = Password(password, encryption_type, self.app, encryption_key)
            self.labels = labels
            self.user_id = self.app.user.id

    def create(self):
        """→ Ajouter une nouvelle entrée de mot de passe."""
        return self.database.credentials.create(self)

    def delete(self):
        """→ Supprimer une entrée de mot de passe."""
        if not self.exists or self.user_id != self.app.user.id: return False
        return self.database.credentials.delete(self.id)

