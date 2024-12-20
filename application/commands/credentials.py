import time

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
            case "remove": self.remove()
            case "edit": self.edit()
            case "show": self.show()
            case "list": self.list()
            case "audit": self.audit()
            # case "history": self.history(self.arguments)
            case "generate": self.generate()
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
        if credential.create(): methods.console("green", "[✔] Succès : Votre credentials a été enregistré avec succès.")
        else: methods.console("bright_red", "[✘] Erreur : Une erreur s'est produite lors de l'enregistrement de votre credentials.")
        return self.instance.command()

    def remove(self):
        """Logique associée à la commande 'remove'."""
        try: id = int(next(iter(self.arguments["args"])))
        except ValueError:
            methods.console("bright_red",f"[✘] Erreur : Éxécution incorrecte de la commande, argument(s) manquant(s) ou incorrect : <id>")
            return self.instance.help("credentials", "remove")

        credential = Credentials(self.instance.app, id=id)
        if not credential.exists: methods.console("bright_red", "[✘] Erreur : Aucun credentials trouvé pour l'ID fourni."); return self.instance.command()
        if not credential.user_id == self.instance.app.user.id: methods.console("bright_red", "[✘] Erreur : Vous n'êtes pas autorisé à supprimer ce credentials."); return self.instance.command()

        if credential.delete(): methods.console("green", "[✔] Succès : Votre credentials a été supprimé avec succès.")
        else: methods.console("bright_red", "[✘] Erreur : Une erreur s'est produite lors de la suppression de votre credential.")
        return self.instance.command()

    def edit(self, args):
        """Logique associée à la commande 'edit'."""
        print(
            f"Modification de l'entrée {args.id} avec les nouveaux détails : site={args.website}, login={args.login}, password={args.password}, label={args.label}")

    def show(self, args):
        """Logique associée à la commande 'show'."""
        print(f"Affichage de l'entrée {args.id}.")

    def list(self, args):
        """Logique associée à la commande 'list'."""
        print(f"Liste des entrées avec filtre par label : {args.label}.")

    def generate(self):
        return True

    def audit(self, args):
        """Logique associée à la commande 'audit'."""
        print(f"Audit des entrées : faible={args.weak}, expirée={args.expired}")
