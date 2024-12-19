from application.user import User
from application.password import Password

class Credentials:
    def __init__(self, app, website: str, login: str, password: str, encryption_type:str):
        self.app = app
        self.database = self.app.database

        self.user:User = self.app.user
        self.user_id:int = self.user.id

        self.website:str = website
        self.login:str = login
        self.password = Password(password, encryption_type, self.app)

