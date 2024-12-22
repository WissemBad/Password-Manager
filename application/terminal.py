import datetime
import shlex

from application.commands.credentials import CredentialsCommand
from application.commands.help import HelpCommand

from application.main import User
from database.main import Database

from utils import methods
from utils import ui


class Terminal:
    commands_directory: str = "./application/commands"
    commands: list[str] = ["exit", "quit", "clear", "help", "credentials"]

    def __init__(self, app) -> None:
        self.app = app
        self.user: User = self.app.user
        self.database: Database = self.app.database


    def main(self) -> None:
        """ → Affichage du terminal."""
        methods.clear_terminal()
        ui.menu_terminal()
        return self.command()


    def command(self) -> None:
        """→ Gestion des commandes du terminal."""
        while True:
            request = input(f"\033[2m[{datetime.datetime.now().strftime('%H:%M:%S')}]\033[0m → {self.user.username}@uncracked: ").strip()
            formatted = self.parse_command(request) if not request == "" else {}
            if not formatted: continue

            command = formatted.get("command", None)
            if command not in self.commands:
                methods.console("red",f"→ '{command}' n'est pas reconnue comme une commande valide.\n\033[3mUtilisez 'help' pour afficher les commandes disponibles.")
                continue

            return self.handle_command(formatted)


    def handle_command(self, request: dict):
        """
        → Traite la commande après validation manuelle.
        :param request: La commande et ses arguments.
        :return: None
        """
        match request.get("command"):
            case "help":
                return HelpCommand(self, request)
            case "exit":
                return self.app.after_connect()
            case "quit":
                return self.app.quit()
            case "clear":
                return self.clear()
            case "credentials":
                return CredentialsCommand(self, request)
            case _:
                return self.command()


    @staticmethod
    def parse_command(command: str) -> dict:
        """
        → Séparation de la commande en arguments dans un dictionnaire.
        :param command: La commande brute sous forme de chaîne.
        :return: Un dictionnaire contenant la commande et ses arguments.
        """
        try:
            command_list = shlex.split(command)  # Utilise shlex pour découper proprement les arguments
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
                    if value and (' ' in value or ',' in value): value = value.replace(",", "").split(" ")
                    i += 2
                else:
                    value = None
                    i += 1
                command_dict["args"][option.lower()] = value
            return command_dict
        except ValueError as error:
            methods.console("red", f"[✘] Erreur : {error}")
            return {}


    def help(self, command: str | None = None, subcommand: str | None = None) -> None:
        """
        → Affiche l'aide générale ou spécifique.
        :param command: La commande principale.
        :param subcommand: La sous-commande.
        :return: None
        """
        HelpCommand(self, {"command": "help", "subcommand": command, "args": {subcommand: None}})
        return self.command()


    def clear(self) -> None:
        """
        → Nettoyage du terminal.
        :return: None
        """
        return self.main()
