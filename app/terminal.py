import string
import time

from utils import methods
from utils import ui

class Terminal:
    def __init__(self, app):
        self.app = app
        self.database = self.app.database

        self.user = self.app.get_user()
        if self.user is None:
            raise Exception("Utilisateur non connecté - Sortie du programme par mesure de sécurité.")

        self.commands = self.get_commands()

    def main(self):
        methods.clear_terminal()
        ui.menu_terminal()
        return self.command()

    def command(self):
        while True:
            request = input(f"→ {self.user.username}@uncracked: ").strip().lower()
            request = request.split(" ")
            print(request)

    def get_commands(self):
        return ["help"]

    def clear(self):
        return self.main()
