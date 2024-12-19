import time

from utils import methods
from utils import ui

from database.main import Database
from security.main import Security

from application.user import User
from application.terminal import Terminal
from application.authentification import Authentification

class Application:
    def __init__(self):
        # → Initialisation des dépendances
        self.database = Database(self)
        self.security = Security(self)

        # → Chargement des modules
        self.auth = Authentification(self)
        self.terminal = None

        # → Variables de session
        self.logged_in = False
        self.user: User or None = None

    def run(self):
        """→ Démarrage de l'application."""
        methods.clear_terminal()
        ui.starting_app()
        methods.pending_load()
        methods.clear_terminal()
        return self.auth.choice()

    def init_dependencies(self):
        """→ Initialiser les dépendances de l'application."""
        self.terminal = Terminal(self)
        self.database.init_dependencies()
        self.security.init_dependencies()

    def after_connect(self):
        """→ Menu principal après connexion."""
        while True:
            self.init_dependencies()
            methods.clear_terminal()
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
                    case 2:
                        if methods.confirm("vous déconnecter"): return self.auth.logout()
                    case _:
                        methods.console("bright_red", "[✘] Erreur : L'option sélectionnée n'existe pas.")
                        time.sleep(1)
            except Exception as error:
                methods.console("bright_red", "[✘] Erreur : Vous devez entrer un chiffre.")
                time.sleep(1)

    def reset(self):
        """→ Réinitialiser les variables de session."""
        self.database.save()
        self.logged_in = False
        self.user = None

        self.database = Database(self)
        self.security = Security(self)

        self.auth = Authentification(self)
        self.terminal = None

    def quit(self):
        """→ Quitter l'application."""
        if methods.confirm("quitter le programme"):
            self.reset()
            methods.clear_terminal(),
            methods.console("green", "[✔] Succès : Vous avez quitté l'application.")
            return exit(0)
        else: return self.auth.choice()


def ask_options():
    options = ["Accéder au terminal", "Définir les réglages", "Se déconnecter"]
    for i, option in enumerate(options):
        print(f"{i}: {option}")
    return True

