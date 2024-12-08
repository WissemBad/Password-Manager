from app import ui
from app import methods
from app.user import User
class App:
    def __init__(self, database):
        self.database = database


        self.logged_in = False
        self.user = None

        self.menu = True
        self.options = {
            "connexion": [
                "Se connecter",
                "Créer un compte",
                "Quitter l'application",
            ]
        }


    def ask_connexion(self):
        if self.logged_in or self.user is not None: return False
        while self.menu:
            methods.clear_terminal()
            ui.menu_connexion(self.options["connexion"])
            try:
                response = int(input("→ ").strip())
                self.menu = False
                methods.clear_terminal()
                return self.connexion(response)
            except ValueError: continue

    def connexion(self, mode: int):
        match mode:
            case 0:
                username, password = ui.menu_login()
                user = User(username, password, self)
                return print("Connexion réussie !") if user.login() else print("Identifiants incorrects !")
            case 1:
                return

    # → Connexion à l'application
    def login(self, user: object):
        self.user = user
        self.logged_in = True
        return True

    # → Déconnexion de l'application
    def logout(self):
        self.user = None
        self.logged_in = False
        return True


