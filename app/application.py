from tkinter import BooleanVar

from utils import methods

from app.user import User

from database.init import Database
from app.authentification import Authentification

class App:
    def __init__(self):
        self.database = Database(self)
        self.auth = Authentification(self)

        self.logged_in = False
        self.user:(User or None) = None

    def after_connect(self):
        methods.clear_terminal()
        methods.console("cyan", f"→ Bienvenue \033[1m{self.user.username}\033[0m\033[36m, votre gestionnaire est prêt !")
        return

    def quit(self):
        self.logged_in = False
        self.user = None
        if methods.confirm("quitter le programme"): return methods.clear_terminal(), methods.console("green", "[✔] Succès : Vous avez quitté l'application.")
        else: return self.auth.choice()

