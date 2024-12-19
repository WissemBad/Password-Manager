import datetime
import os

from utils import methods
from utils import ui

from application.commands.help import Help

class Terminal:
    commands_directory = "./application/commands"
    commands_base = ["exit", "quit", "clear"]

    def __init__(self, app):
        self.app = app
        self.user = self.app.user
        self.database = self.app.database

        self.commands = self.get_commands()

    def get_commands(self):
        """→ Récupération des commandes existantes (by ChatGPT)."""
        commands = [os.path.splitext(file)[0] for file in os.listdir(self.commands_directory) if file.endswith('.py')]
        return self.commands_base + commands

    def main(self):
        """→ Affichage du terminal."""
        methods.clear_terminal()
        ui.menu_terminal()
        return self.command()

    def command(self):
        """→ Gestion des commandes du terminal."""
        while True:
            request = input(f"\033[2m[{datetime.datetime.now().strftime("%H:%M:%S")}]\033[0m → {self.user.username}@uncracked: ").strip().lower()
            formatted = self.split_command(request)
            if not formatted[0] in self.commands: methods.console("red", f"→ '{formatted[0]}' n'est pas reconnue comme une commande valide.\n\033[3mUtilisez 'help' pour afficher les commandes disponibles.")
            match formatted[0]:
                case "help": Help(formatted)
                case "clear": return self.clear()
                case "exit": return self.app.after_connect()
                case "quit": return self.app.quit()

    @staticmethod
    def split_command(command):
        """→ Séparation de la commande en arguments."""
        formatted = []
        split = command.split(" ")
        for item in split:
            if not item.strip(): split.remove(item)
            formatted.append(item)
        return formatted

    def clear(self):
        """→ Nettoyage du terminal."""
        return self.main()