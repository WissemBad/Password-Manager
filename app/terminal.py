import string
import time
import os

from utils import methods
from utils import ui

from app.commands.help import Help

class Terminal:
    def __init__(self, app):
        self.app = app
        self.database = self.app.database

        self.user = self.app.get_user()
        if self.user is None: raise Exception("Utilisateur non connecté - Sortie du programme par mesure de sécurité.")

        self.cmd_directory = "./app/commands"
        self.commands = self.get_commands()

    def main(self):
        methods.clear_terminal()
        ui.menu_terminal()
        return self.command()

    def command(self):
        while True:
            request = input(f"→ {self.user.username}@uncracked: ").strip().lower()
            formatted = split_command(request)
            if not formatted[0] in self.commands: methods.console("red", f"→ '{formatted[0]}' n'est pas reconnue comme une commande valide.\n\033[3mUtilisez 'help' pour afficher les commandes disponibles.")
            match formatted[0]:
                case "help": Help(formatted)
                case "clear": return self.clear()
                case "exit": return self.app.after_connect()
                case "quit": return self.app.quit()

    def get_commands(self):
        commands = [os.path.splitext(file)[0] for file in os.listdir(self.cmd_directory) if file.endswith('.py')]
        base = ["exit", "quit", "clear"]
        return commands + base

    def clear(self):
        return self.main()

def split_command(command):
    formatted = [item for item in command.split(" ") if item.strip()]
    return formatted