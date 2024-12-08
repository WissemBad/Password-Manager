from database.init import Database
from app.application import App

from app import methods
from app import ui

from security.methods import decrypt

Application = App(Database())

def main():
    # Nettoyer le terminal utilisateur
    methods.clear_terminal()

    # Lancer le chargement de l'application
    ui.starting_app()

    # Attendre que l'utilisateur presse une touche
    methods.pending_load()

    # Lancement du chargement de l'application
    ui.loading_app(0.01, 1)

    # Nettoyer le terminal utilisateur
    methods.clear_terminal()

    # Demander l'action à effectuer
    Application.ask_connexion()

if __name__ == "__main__":
    main()
