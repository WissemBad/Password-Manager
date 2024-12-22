import time

from application.main import Application
from application.user import User
from database.main import Database

from utils import ui
from utils import methods


class Authentification:
    def __init__(self, app: Application) -> None:
        self.app: Application = app
        self.database: Database = self.app.database


    def choice(self) -> None:
        """
        → Affiche le menu de choix pour l'authentification et gère les actions.
        :return: None
        """
        while True:
            methods.clear_terminal()
            ui.menu_auth(ask_options)
            try:
                response = int(input("→ ").strip())
                match response:
                    case 0: return self.login()
                    case 1: return self.register()
                    case 2: return self.app.quit()
                    case _: methods.console("bright_red", "[✘] Erreur : L'option sélectionnée n'existe pas."); time.sleep(1.5)
            except ValueError:
                methods.console("bright_red", "[✘] Erreur : Vous devez entrer un chiffre.")
                time.sleep(1.5)
            except Exception as error:
                methods.console("bright_red", f"[✘] Erreur inconnue : {error}")
                time.sleep(1.5)


    def login(self) -> None:
        """
        → Gère le processus de connexion à l'application.
        :return: None
        """
        methods.clear_terminal()
        username, password = ui.menu_login(ask_login)
        user = User(username, password, self.app)
        if user.login(password):
            self.app.logged_in = True
            self.app.user = user
            self.app.user.safety_auth = True
            methods.console("green", "[✔] Succès : Connexion établie !")
            methods.console("bright_yellow", f"[ί] Info : Redirection vers le menu principal...")
            time.sleep(1.8)
            return self.app.after_connect()
        else:
            methods.console("red", "[✘] Erreur : Identifiants incorrects ou inexistants !")
            time.sleep(1.5)
            return self.choice()


    def register(self, repeat: bool = False) -> None:
        """
        → Gère le processus d'enregistrement d'un nouvel utilisateur.
        :param repeat: Booléen qui détermine si l'enregistrement doit être refait.
        :return: None
        """
        methods.clear_terminal()
        username, password, confirm = ui.menu_register(ask_register)

        if not username or not password:
            methods.console("bright_red", "[✘] Erreur : Les champs ne doivent pas être vides.")
            time.sleep(1.5)
            return self.register(repeat) if not repeat else self.choice()

        if password != confirm:
            methods.console("bright_red", "[✘] Erreur : Les mots de passe ne correspondent pas.")
            time.sleep(1.5)
            return self.register(repeat) if not repeat else self.choice()

        user = User(username, password, self.app)
        if user.register():
            methods.console("green", f"[✔] Succès : Votre compte [{username}] a été créé !")
            self.app.logged_in = True
            self.app.user = user
            self.app.user.safety_auth = True
            methods.console("bright_yellow", f"[ί] Info : Redirection vers le menu principal dans 3s...")
            time.sleep(1.8)
            return self.app.after_connect()
        else:
            methods.console("red", f"[✘] Erreur : Le nom d'utilisateur [{username}] est déjà utilisé.")
            time.sleep(1.5)
            return self.register(repeat) if not repeat else self.choice()


    def logout(self) -> None:
        """
        → Déconnexion de l'application et redirection vers l'accueil.
        :return: None
        """
        methods.clear_terminal()
        methods.console("green", f"[✔] Succès : Déconnexion effectuée !\n→ Vos données ont été correctement enregistrées.\n")
        self.app.logged_in = False
        self.app.user = None
        self.app.terminal = None
        methods.console("bright_yellow", f"[ί] Info : Redirection vers l'accueil...")
        time.sleep(3)
        return self.choice()


def ask_login() -> tuple[str, str]:
    """
    → Demande les informations de connexion à l'utilisateur.
    :return: Un tuple contenant le nom d'utilisateur et le mot de passe.
    """
    username = input("→ Nom d'utilisateur : ").strip().lower().replace(" ", "_")
    password = methods.secure_input("→ Mot de passe : ").strip()
    return username, password


def ask_register() -> tuple[str, str, bool]:
    """
    → Demande les informations d'enregistrement de l'utilisateur.
    :return: Un tuple contenant le nom d'utilisateur, le mot de passe, et si les mots de passe correspondent.
    """
    username = input("→ Nom d'utilisateur : ").strip().lower().replace(" ", "_")
    print("----------------------------------")
    password = methods.secure_input("→ Mot de passe : ")
    confirm = methods.secure_input("→ Confirmation : ")
    return username, password, password == confirm


def ask_options() -> bool:
    """
    → Affiche les options disponibles pour l'utilisateur dans le menu d'authentification.
    :return: Toujours True, utilisé pour maintenir la boucle active.
    """
    options = ["Se connecter", "Créer un compte", "Quitter l'application"]
    for i, option in enumerate(options): print(f"{i}: {option}")
    return True