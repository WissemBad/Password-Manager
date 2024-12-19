from utils import methods
from utils import ui

class Help:
    global_commands = (
        ("help", "Afficher la liste des commandes existantes.", "help"),
        ("exit", "Sortie du terminal et retour au menu principal.", "exit"),
        ("quit", "Quitter le gestionnaire et déconnexion de l'application.", "quit"),
        ("credentials", "Gestion des mots de passe dans l'application.", "credentials [options]"),
        ("label", "Gestion des étiquettes dans l'application.", "label [options]")
    )

    sub_commands = [
        [
            "credentials", {
                "add": [ # Ajouter une nouvelle entrée
                    "Ajoute une nouvelle entrée d'identifiants au gestionnaire.",
                    "credentials add --website <url> --login <login> --password <password> --label <label>"
                ],
                "edit": [ # Modifier une entrée existante
                    "Modifie les détails d'une entrée existante.",
                    "credentials edit <id> [--website <url>] [--login <login>] [--password <password>] [--label <label>]"
                ],
                "remove": [ # Supprimer une entrée spécifique
                    "Supprime une entrée spécifique.",
                    "credentials remove <id>"
                ],
                "show": [ # Afficher les détails d'une entrée spécifique
                    "Affiche les détails d'une entrée spécifique.",
                    "credentials show <id>"
                ],
                "list": [ # Liste toutes les entrées enregistrées, avec des options de filtre
                    "Liste toutes les entrées enregistrées, avec des options de filtre.",
                    "credentials list [--label <label>] [--expired] [--strength <min_strength>]"
                ],
                "search": [  # Rechercher une entrée spécifique
                    "Recherche une entrée spécifique dans la base de données.",
                    "credentials search [--label <label>] [--website <website>] [--login <login>]"
                ],
                "audit": [ # Analyse les entrées pour détecter les failles de sécurité (API hasbeenpwned)
                    "Analyse les entrées pour détecter les failles de sécurité (faibles ou expirées).",
                    "credentials audit <password>"
                ],
                "history": [ # Affiche l'historique des modifications d'une entrée
                    "Affiche l'historique des modifications d'une entrée.",
                    "credentials history <website>"
                ],
                "generate": [ # Générer un mot de passe sécurisé
                    "Génère un mot de passe sécurisé pour une nouvelle entrée.",
                    "credentials generate [--length <number>] [--symbols] [--numbers] [--uppercase] [--lowercase]"
            ]
        }]
    ]

    def __init__(self, args):
        self.arguments = args

        # Commandes globales
        self.global_help() if len(self.arguments) == 1 else self.specific_help(self.arguments[1])

    def global_help(self):
        """→ Afficher l'aide globale."""
        print("╔════════════════════════════════════╗")
        print("║             \033[1mMENU D'AIDE\033[0m            ║")
        print("║  Voici les commandes existantes :  ║")
        print("╚════════════════════════════════════╝")
        for command in self.global_commands:
            print(f"  → \033[100;1m{command[0]}\033[0m : \033[3m{command[1]}\033[0m\n    \033[4mUsage :\033[0m \033[100m{command[2]}\033[0m")
            print("")

    def specific_help(self, main_command):
        """→ Afficher l'aide spécifique."""
        ui.help_specific()
        found = False

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
                found = True

        # Si aucune correspondance spécifique n'a été trouvée, vérifier dans les commandes globales
        if not found:
            for command in self.global_commands:
                cmd_name, description, usage = command
                if cmd_name == main_command:
                    print(f"  → \033[100;1m{cmd_name}\033[0m : \033[3m{description}\033[0m\n    \033[4mUsage :\033[0m \033[100m{usage}\033[0m")
                    print("")
                    found = True

        # Si aucune correspondance n'est trouvée, afficher un message d'erreur
        if not found:
            methods.console("red", f"[✘] Erreur : La commande '{main_command}' n'existe pas.")


