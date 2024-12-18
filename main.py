import os
from app.application import App
from dotenv import load_dotenv

from utils import methods
from utils import ui

Application = App()

if __name__ == "__main__":
    # Vérifie si .env existe
    if not os.path.exists(".env"): Application.security.manager.initialize_security()


    # Lancer l'application
    load_dotenv(), Application.run()
