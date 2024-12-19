import datetime
import os
import shlex
import argparse

from utils import methods
from utils import ui

from application.commands.help import Help
from application.commands.credentials import Credentials  # Assurez-vous que Credentials utilise argparse
from application.commands.label import Label  # Si tu as une commande label, ajoute-la ici

class Terminal:
    commands_directory = "./application/commands"
    commands_base = ["exit", "quit", "clear"]

    def __init__(self, app):
        self.app = app
        self.user = self.app.user
        self.database = self.app.database

        self.parser = self.create_parser()

    @staticmethod
    def create_parser():
        """ → Crée le parser principal et les sous-commandes."""
        parser = argparse.ArgumentParser(description="Gestionnaire de commandes.")
        subparsers = parser.add_subparsers(dest="command", required=False)

        # - Crée les sous-commandes associées à 'help'
        credentials_parser = subparsers.add_parser('credentials', help="Gestion des mots de passe")
        Credentials(credentials_parser)

        # - Crée les sous-commandes associées à 'label'
        label_parser = subparsers.add_parser('label', help="Gestion des étiquettes")
        Label(label_parser)
        return parser

    def get_commands(self):
        """→ Récupération des commandes existantes (avec argparse)."""
        commands = self.commands_base
        for command_group in os.listdir(self.commands_directory):
            if command_group.endswith('.py'):
                command_name = os.path.splitext(command_group)[0]
                commands.append(command_name)
        return commands

    def main(self):
        """→ Affichage du terminal."""
        methods.clear_terminal()
        ui.menu_terminal()
        return self.command()

    def command(self):
        """→ Gestion des commandes du terminal avec argparse."""
        while True:
            request = input(f"\033[2m[{datetime.datetime.now().strftime('%H:%M:%S')}]\033[0m → {self.user.username}@uncracked: ").strip().lower()
            formatted = self.split_command(request)
            if not formatted: continue

            if formatted[0] not in self.get_commands():
                methods.console("red", f"→ '{formatted[0]}' n'est pas reconnue comme une commande valide.\n\033[3mUtilisez 'help' pour afficher les commandes disponibles.")
                continue
            try:
                args, unknown = self.parser.parse_known_args(formatted)
                if args.command is None: methods.console("red", f"→ '{formatted[0]}' n'est pas reconnue comme une commande valide.\n\033[3mUtilisez 'help' pour afficher les commandes disponibles.")
                else: self.handle_command(args)
            except SystemExit: pass

    def handle_command(self, args):
        """→ Traite la commande après validation par argparse."""
        match args.command:
            case "help": Help(args)
            case "clear": return self.clear()
            case "exit": return self.app.after_connect()
            case "quit": return self.app.quit()
            # Ex : case "credentials": Credentials.handle(args) ou autre logique

    @staticmethod
    def split_command(command):
        """→ Séparation de la commande en arguments à l'aide de shlex.split."""
        try:
            return shlex.split(command)
        except ValueError as error:
            methods.console("red", f"[✘] Erreur : {error}")
            return []

    def clear(self):
        """→ Nettoyage du terminal."""
        return self.main()
