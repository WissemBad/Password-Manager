import os
from application.main import Application

Application = Application()

if __name__ == "__main__":
    # Vérifie si .env existe
    if not os.path.exists(".env"): Application.security.manager.initialize_security()

    # Lancer l'application
    Application.run()
