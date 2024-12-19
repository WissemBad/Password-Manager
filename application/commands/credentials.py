from utils import methods
from application.credentials import Credentials

class CredentialsCommand:
    def __init__(self, terminal, args):
        self.instance = terminal
        self.arguments = args

        self.handle()

    def handle(self):
        match self.arguments["subcommand"]:
            case "add": self.add()
            case "remove": self.remove(self.arguments)
            case "edit": self.edit(self.arguments)
            case "show": self.show(self.arguments)
            case "list": self.list_entries(self.arguments)
            case "audit": self.audit(self.arguments)
            # case "history": self.history(self.arguments)
            # case "generate": self.generate(self.arguments)
            case _: self.instance.help("credentials")

    def add(self):
        """Logique associée à la commande 'add'."""
        # - Vérification des arguments manquants
        required_args = ["website", "login", "password", "encryption_type"]
        missing_args = [arg for arg in required_args if arg not in self.arguments["args"].keys()]
        if missing_args: return methods.console("bright_red", f"[✘] Erreur : Argument(s) manquant(s) : {', '.join(missing_args)}"), self.instance.help("credentials", "add")

        # - Récupérer et normaliser les données facultatives
        labels = self.arguments["args"].get("label", [])
        labels = [label.lower() for label in labels] if labels else []
        encryption_key = None
        try: encryption_key = int(self.arguments["args"].get("encryption_key")) if self.arguments["args"].get("encryption_key") else None
        except ValueError: methods.console("yellow", "[ί] Attention : La clé de chiffrement doit être un nombre entier.\nUtilisation de la clé de chiffrement par défaut.")

        # - Construction des données
        data = {
            "id": methods.auto_increment(self.instance.app.database.credentials.data),
            "website": self.arguments["args"]["website"].lower(),
            "login": self.arguments["args"]["login"],
            "password": self.arguments["args"]["password"],
            "encryption_type": self.arguments["args"]["encryption_type"].upper(),
            "encryption_key": encryption_key,
            "labels": labels
        }

        # - Vérification du type de chiffrement
        if data["encryption_type"] not in ["AES", "RSA", "CESAR"]:
            methods.console("bright_red", "[✘] Erreur : Type de chiffrement invalide. Utilisez 'AES', 'RSA' ou 'CESAR'.")
            return self.instance.help("credentials", "add")

        credential = Credentials(self.instance.app, **data)
        if credential.create(): methods.console("green", "[✔] Succès : Vos credentials ont été enregistrés avec succès.")
        else: methods.console("bright_red", "[✘] Erreur : Une erreur s'est produite lors de l'enregistrement de vos credentials.")
        return self.instance.command()

    def remove(self, args):
        """Logique associée à la commande 'remove'."""
        required_args = ["id"]
        missing_args = [arg for arg in required_args if arg not in self.arguments["args"].keys()]
        if missing_args:
            methods.console("bright_red", f"[✘] Erreur : Éxécution incorrecte de la commande, argument(s) manquant(s) : {', '.join(missing_args)}")
            self.instance.help("credentials", "remove")

        print(f"Suppression de l'entrée {args.id}.")

    def edit(self, args):
        """Logique associée à la commande 'edit'."""
        print(
            f"Modification de l'entrée {args.id} avec les nouveaux détails : site={args.website}, login={args.login}, password={args.password}, label={args.label}")

    def show(self, args):
        """Logique associée à la commande 'show'."""
        print(f"Affichage de l'entrée {args.id}.")

    def list_entries(self, args):
        """Logique associée à la commande 'list'."""
        print(f"Liste des entrées avec filtre par label : {args.label}.")

    def audit(self, args):
        """Logique associée à la commande 'audit'."""
        print(f"Audit des entrées : faible={args.weak}, expirée={args.expired}")
