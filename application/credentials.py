from application.user import User
from application.password import Password

class Credentials:
    def __init__(self, app, id: int, website: str = None, login: str = None, password: str = None, encryption_type: str = None, encryption_key: str = None, labels: list = []):
        self.app = app
        self.database = self.app.database

        self.id:int = id
        self.exists = self.database.credentials.exists(self.id)

        self.user = self.app.user
        self.user_id = self.user.id

        if self.exists:
            self.data = self.database.credentials.get_by_id(self.id)
            self.website = self.data["website"]
            self.login = self.data["login"]
            self.labels = self.data["labels"]
            self.password_encrypted = Password(self.data["password"], self.data["encryption_type"], self.app, self.data["encryption_key"])
            self.password_history = self.data["history"]
        else:
            self.website:str = website
            self.login:str = login
            self.password = Password(password, encryption_type, self.app, encryption_key)
            self.credentials = labels

    def create(self):
        """→ Ajouter une nouvelle entrée de mot de passe."""
        return self.database.credentials.create(self)

