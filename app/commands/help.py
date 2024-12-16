from utils import methods

class Help:
    def __init__(self, args):
        self.arguments = args

        self.global_commands = (
            ("help", "Afficher la liste des commandes existantes.", "help"),
            ("exit", "Sortie du terminal et retour au menu principal.", "exit"),
            ("quit", "Quitter le gestionnaire et déconnexion de l'application.", "quit"),
            ("credentials", "Gestion des mots de passe dans l'application.", "password [options]"),
            ("label", "Gestion des étiquettes dans l'application.", "label [options]")
        )

        self.sub_commands = [
            ["credentials", {
                "add": [
                    "Ajoute une nouvelle entrée d'identifiants au gestionnaire.",
                    "credentials add --website <url> --login <login> --password <password> --label <label>"
                ],
                "edit": [
                    "Modifie les détails d'une entrée existante.",
                    "credentials edit <id> [--website <url>] [--login <login>] [--password <password>] [--label <label>]"
                ],
                "remove": [
                    "Supprime une entrée spécifique.",
                    "credentials remove <id>"
                ],
                "show": [
                    "Affiche les détails d'une entrée spécifique.",
                    "credentials show <id>"
                ],
                "list": [
                    "Liste toutes les entrées enregistrées, avec des options de filtre.",
                    "credentials list [--label <label>] [--expired] [--strength <min_strength>]"
                ],
                "audit": [
                    "Analyse les entrées pour détecter les failles de sécurité (faibles ou expirées).",
                    "credentials audit [--weak] [--expired]"
                ],
                "history": [
                    "Affiche l'historique des modifications d'une entrée.",
                    "credentials history <id>"
                ],
                "generate": [
                    "Génère un mot de passe sécurisé pour une nouvelle entrée.",
                    "credentials generate [--length <number>] [--symbols] [--numbers] [--uppercase] [--lowercase]"
                ]
            }]
        ]

        # Affiche l'aide globale ou spécifique
        self.global_help() if len(self.arguments) == 1 else self.specific_help(self.arguments[1])

    def global_help(self):
        print("╔════════════════════════════════════╗")
        print("║             \033[1mMENU D'AIDE\033[0m            ║")
        print("║  Voici les commandes existantes :  ║")
        print("╚════════════════════════════════════╝")
        for command in self.global_commands:
            print(f"  → \033[100;1m{command[0]}\033[0m : \033[3m{command[1]}\033[0m\n    \033[4mUsage :\033[0m \033[100m{command[2]}\033[0m")
            print("")

    def specific_help(self, main_command):
        print("╔════════════════════════════════════╗")
        print("║             \033[1mMENU D'AIDE\033[0m            ║")
        print("║     Description des commandes :    ║")
        print("╚════════════════════════════════════╝")

        found = False  # Indique si une correspondance a été trouvée

        # Vérifier dans les sous-commandes spécifiques
        for command_group in self.sub_commands:
            group_name, subcommands = command_group
            if group_name == main_command:
                print(f"\033[1;40;97m → Commande : '{group_name}' :\033[0m")
                for subcommand, details in subcommands.items():
                    description, usage = details
                    print(f"  • \033[100;1m{subcommand}\033[0m : \033[3m{description}\033[0m")
                    print(f"    \033[4mUsage\033[0m : \033[100m{usage}\033[0m")
                    print("")
                found = True  # Marquer la correspondance comme trouvée

        # Si aucune correspondance spécifique n'a été trouvée, vérifier dans les commandes globales
        if not found:
            for command in self.global_commands:
                cmd_name, description, usage = command
                if cmd_name == main_command:
                    print(f"  → \033[100;1m{cmd_name}\033[0m : \033[3m{description}\033[0m\n    \033[4mUsage :\033[0m \033[100m{usage}\033[0m")
                    print("")
                    found = True  # Marquer la correspondance comme trouvée

        # Si aucune correspondance n'est trouvée, afficher un message d'erreur
        if not found:
            methods.console("red", f"[✘] Erreur : La commande '{main_command}' n'existe pas.")


