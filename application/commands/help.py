from utils import methods, ui


class HelpCommand:
    def __init__(self, terminal, args):
        self.instance = terminal
        self.arguments = args

        # Commandes globales
        self.global_commands = (
            ("help", "Afficher la liste des commandes existantes.", "help [<command>] [<subcommand>]"),
            ("exit", "Sortie du terminal et retour au menu principal.", "exit"),
            ("quit", "Quitter le gestionnaire et déconnexion de l'application.", "quit"),
            ("clear","Nettoyer le terminal de l'application", "clear"),
            ("credentials", "Gestion des mots de passe dans l'application.", "credentials --options")
        )

        # Commandes spécifiques
        self.sub_commands = [
            (
                "credentials",
                {
                    "add": (
                        "Ajoute une nouvelle entrée d'identifiants au gestionnaire.",
                        "credentials add --website <url> --login <login> --password <password> --encryption_type <AES/RSA/CESAR> [--cesar_key <key>] [--labels <labels>]",
                        "credentials add --website example.com --login admin --password adminPass --encryption_type AES --labels 'Important, Panel, Banque'"
                    ),
                    "edit": (
                        "Modifie les détails d'une entrée existante.",
                        "credentials edit <id> [--website <url>] [--login <login>] [--password <password>] [--labels <labels>] [--encryption_type <AES/RSA/CESAR>] [--cesar_key <key>]",
                        "credentials edit 123 --website imt-atlantique.fr --login admin --password adminPass --labels School"
                    ),
                    "remove": (
                        "Supprime une entrée spécifique.",
                        "credentials remove <id>",
                        "credentials remove 123"
                    ),
                    "show": (
                        "Affiche les détails d'une entrée spécifique.",
                        "credentials show <id> [--decrypted]",
                        "credentials show 123 --decrypted"
                    ),
                    "list": (
                        "Liste toutes les entrées enregistrées, avec des options de filtre.",
                        "credentials list [--website <website>] [--login <login>] [--labels <labels>] [--strength <1-4>] [--encryption_type <AES/RSA/CESAR>]",
                        "credentials list --website imt-nord-europe.fr --labels 'Important, School'"
                    ),
                    "audit": (
                        "Analyse les entrées pour détecter les failles de sécurité.",
                        "credentials audit <id>",
                        "credentials audit 123"
                    ),
                    "history": (
                        "Affiche l'historique des modifications d'une entrée.",
                        "credentials history <id> <history_id> [--decrypted]",
                        "credentials history 123 456 --decrypted"
                    ),
                    "generate": (
                        "Génère un mot de passe sécurisé pour une nouvelle entrée.",
                        "credentials generate [--strength <1-4>] [--use_dictionary] [--no_numbers] [--no_mixed_case] [--length <length>]",
                        "credentials generate --strength 4 --use_dictionary --no_numbers --no_specials --no_mixed_case --length 12"
                    )
                }
            )
        ]

        self.handle()


    def handle(self):
        """→ Gestion des commandes d'aide."""
        if self.arguments["subcommand"] is None: return self.global_help()
        else: return self.specific_help(self.arguments["subcommand"]) if not self.arguments["args"] else self.specific_help(self.arguments["subcommand"], next(iter(self.arguments["args"])))


    def global_help(self):
        """→ Affiche l'aide générale."""
        ui.help_global()
        for command in self.global_commands:
            print( f"  → \033[100;1m{command[0]}\033[0m : \033[3m{command[1]}\033[0m\n    \033[4mUsage :\033[0m \033[100m{command[2]}\033[0m\n")
        return self.instance.command()


    def specific_help(self, main_command, sub_command=None):
        """→ Affiche l'aide spécifique."""
        found = False

        if sub_command is None:
            for group_name, subcommands in self.sub_commands:
                if group_name == main_command:
                    ui.help_specific()
                    print(f"\033[1;40;97m → Commande : '{group_name}' :\033[0m")
                    for subcommand, (description, usage, example) in subcommands.items():
                        print(f"  • \033[100;1m{subcommand}\033[0m : \033[3m{description}\033[0m")
                        print(f"    \033[4mUsage\033[0m : \033[100m{usage}\033[0m")
                        print(f"    \033[2;4mExemple\033[0m : \033[2m{example}\033[0m\n")
                    found = True

            if not found:
                for cmd_name, description, usage in self.global_commands:
                    if cmd_name == main_command:
                        print(f"  → \033[100;1m{cmd_name}\033[0m : \033[3m{description}\033[0m\n    \033[4mUsage :\033[0m \033[100m{usage}\033[0m\n")
                        found = True

            if not found: methods.console("red", f"[✘] Erreur : La commande '{main_command}' n'existe pas.")
        else:
            for group_name, subcommands in self.sub_commands:
                if group_name == main_command:
                    for subcommand, (description, usage, example) in subcommands.items():
                        if subcommand == sub_command:
                            print(f"\033[1;40;97m → Commande : '{group_name} {subcommand}' :\033[0m \033[3m{description}\033[0m")
                            print(f"  • \033[4mUsage\033[0m : \033[100m{usage}\033[0m")
                            print(f"  • \033[2;4mExemple\033[0m : \033[2m{example}\033[0m\n")
                            found = True


            if not found: methods.console("red", f"[✘] Erreur : La commande '{main_command} {sub_command}' n'existe pas.")
        return self.instance.command()