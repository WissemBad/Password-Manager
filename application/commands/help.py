import argparse
from utils import methods

from application.commands.credentials import Credentials
from application.commands.label import Label


class Help:
    def __init__(self, args):
        self.arguments = args
        self.parser = self.create_parser()

        # Affiche l'aide globale ou spécifique
        self.global_help() if len(self.arguments) == 1 else self.specific_help(self.arguments[1])

    def create_parser(self):
        """Crée le parser principal avec les sous-commandes."""
        parser = argparse.ArgumentParser(description="Gestionnaire de commandes.")
        subparsers = parser.add_subparsers(dest="command", required=False)

        # Créer une instance de la classe Credentials (et d'autres commandes)
        Credentials(subparsers)
        Label(subparsers)

        return parser

    def global_help(self):
        """Affiche l'aide globale pour toutes les commandes."""
        print("╔════════════════════════════════════╗")
        print("║             \033[1mMENU D'AIDE\033[0m            ║")
        print("║  Voici les commandes existantes :  ║")
        print("╚════════════════════════════════════╝")

        # Affiche les commandes globales
        for command in self.parser._actions:
            if isinstance(command, argparse._SubParsersAction):
                for subcommand in command._choices_actions:
                    print(
                        f"  → \033[100;1m{subcommand.dest}\033[0m : \033[3m{self.get_command_description(subcommand.dest)}\033[0m")
                    print(f"    \033[4mUsage :\033[0m \033[100m{subcommand.dest} [options]\033[0m")
                    print("")

    def get_command_description(self, command_name):
        """Retourne la description associée à chaque commande."""
        descriptions = {
            "help": "Afficher la liste des commandes existantes.",
            "exit": "Sortie du terminal et retour au menu principal.",
            "quit": "Quitter le gestionnaire et déconnexion de l'application.",
            "credentials": "Gestion des mots de passe dans l'application.",
            "label": "Gestion des étiquettes dans l'application."
        }
        return descriptions.get(command_name, "Pas de description disponible.")

    def specific_help(self, main_command):
        """Affiche l'aide spécifique pour une commande donnée."""
        print("╔════════════════════════════════════╗")
        print("║             \033[1mMENU D'AIDE\033[0m            ║")
        print("║     Description des commandes :    ║")
        print("╚════════════════════════════════════╝")

        found = False  # Indique si une correspondance a été trouvée

        # Vérifier dans les sous-commandes spécifiques
        for command_group in self.parser._actions:
            if isinstance(command_group, argparse._SubParsersAction):
                for subcommand in command_group._choices_actions:
                    if subcommand.dest == main_command:
                        print(f"\033[1;40;97m → Commande : '{main_command}' :\033[0m")
                        print(
                            f"  • \033[100;1m{subcommand.dest}\033[0m : \033[3m{self.get_command_description(subcommand.dest)}\033[0m")
                        print(f"    \033[4mUsage\033[0m : \033[100m{subcommand.dest} [options]\033[0m")
                        found = True
                        print("")

        # Si aucune correspondance spécifique n'a été trouvée, afficher un message d'erreur
        if not found:
            methods.console("red", f"[✘] Erreur : La commande '{main_command}' n'existe pas.")
