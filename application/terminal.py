import datetime
import os
import shlex

from utils import methods
from utils import ui

from application.commands.help import HelpCommand
from application.commands.credentials import CredentialsCommand

class Terminal:
    commands_directory = "./application/commands"
    commands_base = ["exit", "quit", "clear"]

    def __init__(self, app):
        self.app = app
        self.user = self.app.user
        self.database = self.app.database

        self.commands = self.load_commands()

    def main(self):
        """→ Affichage du terminal."""
        methods.clear_terminal()
        ui.menu_terminal()
        return self.command()

    def load_commands(self):
        """→ Chargement des commandes disponibles."""
        found_commands = self.commands_base
        for file in os.listdir(self.commands_directory):

            if file.endswith(".py") and file != "__init__.py":
                command = file.replace(".py", "")
                found_commands.append(command)
        return found_commands

    def command(self):
        """→ Gestion des commandes du terminal."""
        while True:
            request = input(f"\033[2m[{datetime.datetime.now().strftime('%H:%M:%S')}]\033[0m → {self.user.username}@uncracked: ").strip()
            formatted = self.parse_command(request)
            if not formatted: continue

            command = formatted.get("command")
            if command not in self.commands:
                methods.console("red", f"→ '{command}' n'est pas reconnue comme une commande valide.\n\033[3mUtilisez 'help' pour afficher les commandes disponibles.")
                continue

            self.handle_command(formatted)

    def handle_command(self, request: dict):
        """→ Traite la commande après validation manuelle."""
        match request.get("command"):
            case "help": return HelpCommand(self, request)
            case "exit": return self.app.after_connect()
            case "quit": return self.app.quit()
            case "clear": return self.clear()
            case "credentials": return CredentialsCommand(self, request)

    def help(self, command=None, subcommand=None):
        """→ Affiche l'aide générale ou spécifique."""
        HelpCommand(self, {"command": "help", "subcommand": command, "args": {subcommand: None}})
        return self.command()

    @staticmethod
    def parse_command(command):
        """→ Séparation de la commande en arguments dans un dictionnaire."""
        try:
            command_list = shlex.split(command)
            command_dict = {
                "command": command_list[0],
                "subcommand": command_list[1] if len(command_list) > 1 and not command_list[1].startswith('--') else None,
                "args": {}
            }

            i = 2 if command_dict["subcommand"] else 1
            while i < len(command_list):
                option = command_list[i].lstrip('--')
                if i + 1 < len(command_list) and not command_list[i + 1].startswith('--'):
                    value = command_list[i + 1]
                    if value and (' ' in value or ',' in value): value = [v.strip() for v in value.replace(',', ' ').split()]
                    i += 2
                else:
                    value = None
                    i += 1
                command_dict["args"][option.lower()] = value
            return command_dict
        except ValueError as error:
            methods.console("red", f"[✘] Erreur : {error}")
            return {}

    def clear(self):
        """→ Nettoyage du terminal."""
        return self.main()