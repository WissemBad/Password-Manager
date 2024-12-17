from app.application import App
from dotenv import load_dotenv

from utils import methods
from utils import ui

Application = App()
load_dotenv()

def main():
    # Nettoyer le terminal utilisateur
    methods.clear_terminal()

    # Lancer le chargement de l'application
    ui.starting_app()

    # Attendre que l'utilisateur presse une touche
    methods.pending_load()

    # Lancement du chargement de l'application
    # ui.loading_app(0.005, 0.1,0.2)

    # Nettoyer le terminal utilisateur
    methods.clear_terminal()

    # Demander l'action à effectuer
    Application.auth.choice()

if __name__ == "__main__":
    main()
