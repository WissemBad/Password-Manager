import time

from utils import ui
from utils import methods

from app.user import User

class Authentification:
    def __init__(self, app):
        self.app = app
        self.database = self.app.database

    # → Sélection de la méthode d'authentification
    def choice(self):
        methods.clear_terminal()
        ui.menu_auth(ask_options)
        try:
            response = int(input("→ ").strip())
            match response:
                case 0:
                    return self.login()
                case 1:
                    return self.register()
                case 2:
                    return self.app.quit()
                case _:
                    methods.console("bright_red", "[✘] Erreur : L'option sélectionnée n'existe pas.")
                    time.sleep(1.5)
                    return self.choice()
        except Exception as error:
            methods.console("bright_red", "[✘] Erreur : Vous devez entrer un chiffre.")
            print(error)
            time.sleep(1.5)
            return self.choice()

    # → Connexion à l'application
    def login(self):
        methods.clear_terminal()
        username, password = ui.menu_login(ask_login)
        user = User(username, password, self.app)
        if user.login():
            self.app.logged_in = True
            self.app.user = user
            methods.console("green", "[✔] Succès :  Connexion établie !")
            methods.console("bright_yellow", f"[🛈] Info : Redirection vers le menu principal...")
            time.sleep(1.8)
            return self.app.after_connect()
        else:
            methods.console("red", "[✘] Erreur : Identifiants incorrects ou inexistants !")
            time.sleep(1.5)
            return self.choice()

    # → Enregistrement à l'application
    def register(self, repeat=False):
        methods.clear_terminal()
        username, password, confirm = ui.menu_register(ask_register)

        if password == "" or username == "":
            methods.console("bright_red", "[✘] Erreur : Les champs ne doivent pas être vides.")
            return time.sleep(1.5), self.register(repeat) if not repeat else self.choice()
        if not confirm:
            methods.console("bright_red", "[✘] Erreur : Les mots de passe ne correspondent pas.")
            return time.sleep(1.5), self.register(repeat) if not repeat else self.choice()

        user = User(username, password, self.app)
        if user.register():
            methods.console("green", f"[✔] Succès : Votre compte [{username}] a été créé !")
            self.app.logged_in = True
            self.app.user = user
            methods.console("bright_yellow", f"[🛈] Info : Redirection vers le menu principal dans 3s...")
            time.sleep(1.8)
            return self.app.after_connect()
        else:
            methods.console("red", f"[✘] Erreur : Le nom d'utilisateur est déjà utilisé.")
            return time.sleep(1.5), self.register(repeat) if not repeat else self.choice()

    # → Déconnexion de l'application
    def logout(self):
        methods.clear_terminal()
        methods.console("green", f"[✔] Succès : Déconnexion effectuée !\n→ Vos données ont été correctement enregistrées.\n")
        self.app.logged_in = False
        self.app.user = None
        self.app.terminal = None
        methods.console("bright_yellow", f"[🛈] Info : Redirection vers l'accueil...")
        time.sleep(3)
        return self.choice()

def ask_login():
    username = input("→ Nom d'utilisateur : ").strip().lower().replace(" ", "_")
    password = methods.secure_input("→ Mot de passe : ").strip()
    return username, password

def ask_register():
    username = input("→ Nom d'utilisateur : ").strip().lower().replace(" ", "_")
    print("----------------------------------")
    password = methods.secure_input("→ Mot de passe : ")
    confirm = methods.secure_input("→ Confirmation : ")
    return username, password, password == confirm

def ask_options():
    options = ["Se connecter", "Créer un compte", "Quitter l'application"]
    for i, option in enumerate(options):
        print(f"{i}: {option}")
    return True