import time

from utils import methods
from utils import ui

from database.main import Database
from security.main import Security

from app.user import User
from app.terminal import Terminal
from app.authentification import Authentification

class App:
    def __init__(self):
        self.database = Database(self)
        self.security = Security(self)

        self.auth = Authentification(self)
        self.terminal = None

        self.logged_in = False
        self.user = None

    def run(self):
        """→ Démarrage de l'application."""
        methods.clear_terminal()
        ui.starting_app()
        methods.pending_load()
        methods.clear_terminal()
        return self.auth.choice()

    def after_connect(self):
        methods.clear_terminal()
        self.terminal = Terminal(self)

        methods.console("cyan", f"→ Bienvenue \033[1m{self.user.username}\033[0m\033[36m, votre gestionnaire est prêt !")
        ui.menu_main(ask_options)
        try:
            response = int(input("→ ").strip())
            match response:
                case 0:
                    return self.terminal.main()
                case 1:
                    methods.console("bright_red", "[✘] Erreur : La fonction n'est pas encore implémentée.")
                    time.sleep(1)
                    return self.after_connect()
                case 2:
                    return self.auth.logout() if methods.confirm("vous déconnecter") else self.after_connect()
                case _:
                    methods.console("bright_red", "[✘] Erreur : L'option sélectionnée n'existe pas.")
                    time.sleep(1)
                    return self.after_connect()
        except ValueError as e:
            methods.console("bright_red", "[✘] Erreur : Vous devez entrer un chiffre.")
            time.sleep(1)
            return self.after_connect()

    def get_user(self):
        return self.user

    def quit(self):
        self.logged_in = False
        self.user = None
        if methods.confirm("quitter le programme"): return methods.clear_terminal(), methods.console("green", "[✔] Succès : Vous avez quitté l'application.")
        else: return self.auth.choice()

def ask_options():
    options = ["Accéder au terminal", "Définir les réglages", "Se déconnecter"]
    for i, option in enumerate(options):
        print(f"{i}: {option}")
    return True

