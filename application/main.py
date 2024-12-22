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
        # Initialisation des dépendances
        self.database = Database(self)
        self.security = Security(self)

        # Chargement des modules
        self.auth = Authentification(self)
        self.terminal = None

        # Variables de session
        self.logged_in = False
        self.user: User or None = None


    def run(self):
        """→ Démarre l'application avec l'interface d'authentification."""
        methods.clear_terminal()
        ui.starting_app()
        methods.pending_load()
        methods.clear_terminal()
        return self.auth.choice()


    def init_dependencies(self):
        """→ Initialise les dépendances nécessaires après connexion."""
        if not self.logged_in or not self.user.safety_auth:
            methods.console("bright_red", "[✘] Erreur de sécurité : Tentative de connexion interdite interceptée.")
            exit(0)
        self.terminal = Terminal(self)
        self.database.init_dependencies()
        self.security.init_dependencies()
        self.user.init_dependencies()


    def after_connect(self):
        """ → Menu principal après une connexion réussie."""
        while True:
            self.init_dependencies()
            methods.clear_terminal()
            methods.console("cyan", f"→ Bienvenue \033[1m{self.user.username}\033[0m\033[36m, votre gestionnaire est prêt !")
            ui.menu_main(ask_options)
            try:
                response = int(input("→ ").strip())
                match response:
                    case 0:  # Accéder au terminal
                        try: return self.terminal.main()
                        except Exception as error:
                            methods.console("bright_red", f"[✘] Erreur inconnue liée au terminal : {error}")
                            time.sleep(1)
                    case 1:  # Définir les réglages (non implémenté)
                        methods.console("bright_red", "[✘] Erreur : La fonction n'est pas encore implémentée.")
                        time.sleep(1)
                    case 2:  # Déconnexion
                        if methods.confirm("vous déconnecter"):
                            return self.auth.logout()
                    case _:  # Option invalide
                        methods.console("bright_red", "[✘] Erreur : L'option sélectionnée n'existe pas.")
                        time.sleep(1)
            except ValueError:
                methods.console("bright_red", "[✘] Erreur : Vous devez entrer un chiffre.")
                time.sleep(1)
            except Exception as error:
                methods.console("bright_red", f"[✘] Erreur inconnue : {error}")
                time.sleep(1)


    def reset(self):
        """ → Réinitialise les variables de session et recharge les modules nécessaires."""
        self.database.save()
        self.logged_in = False
        self.user = None

        self.database = Database(self)
        self.security = Security(self)

        self.auth = Authentification(self)
        self.terminal = None


    def quit(self):
        """→ Quitte proprement l'application après confirmation."""
        if methods.confirm("quitter le programme"):
            self.reset()
            methods.clear_terminal()
            methods.console("green", "[✔] Succès : Vous avez quitté l'application.")
            exit(0)
        else: return self.auth.choice()


def ask_options():
    """
    → Affiche les options du menu principal.
    :return: Toujours True, pour garantir l'affichage correct.
    """
    options = ["Accéder au terminal", "Définir les réglages", "Se déconnecter"]
    for i, option in enumerate(options): print(f"{i}: {option}")
    return True
