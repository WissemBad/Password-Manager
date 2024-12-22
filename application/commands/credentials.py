from utils import methods, ui

from application.credentials import Credentials
from application.password import generate_password

class CredentialsCommand:
    def __init__(self, terminal, args: dict[str, dict[str, str | int]]):
        self.instance = terminal
        self.arguments = args
        self.handle()


    def handle(self) -> None:
        """
        → Gère l'exécution de la commande en fonction de la 'subcommand'.
        :return: Rien
        """
        match self.arguments["subcommand"]:
            case "add": self.add()
            case "remove": self.remove()
            case "edit": self.edit()
            case "show": self.show()
            case "list": self.list()
            case "audit": self.audit()
            case "generate": self.generate()
            case _: self.instance.help("credentials")


    def add(self) -> None:
        """
        → Logique associée à la commande 'add'.
        :return: Rien
        """
        required_args = ["website", "login", "password", "encryption_type"]
        missing_args = [arg for arg in required_args if arg not in self.arguments["args"].keys()]
        if missing_args: methods.console("bright_red", f"[✘] Erreur : Argument(s) manquant(s) : {', '.join(missing_args)}"); return self.instance.help("credentials", "add")

        labels = self.arguments["args"].get("label", [])
        if not isinstance(labels, list): labels = [labels]
        labels = [label.lower() for label in labels] if labels else []
        encryption_key = None
        try: encryption_key = int(self.arguments["args"].get("encryption_key")) if self.arguments["args"].get("encryption_key") else None
        except ValueError: methods.console("yellow", "[ί] Attention : La clé de chiffrement doit être un nombre entier.\nUtilisation de la clé de chiffrement par défaut.")

        data = {
            "id": methods.auto_increment(self.instance.app.database.credentials.data),
            "website": self.arguments["args"]["website"].lower(),
            "login": self.arguments["args"]["login"],
            "password": self.arguments["args"]["password"],
            "encryption_type": self.arguments["args"]["encryption_type"].upper(),
            "encryption_key": encryption_key,
            "labels": labels
        }

        if data["encryption_type"] not in ["AES", "RSA", "CESAR"]:
            methods.console("bright_red", "[✘] Erreur : Type de chiffrement invalide. Utilisez 'AES', 'RSA' ou 'CESAR'.")
            return self.instance.help("credentials", "add")

        credential = Credentials(self.instance.app, **data)
        if credential.create(): methods.console("green", "[✔] Succès : Votre credentials a été enregistré avec succès.")
        else: methods.console("bright_red", "[✘] Erreur : Une erreur s'est produite lors de l'enregistrement de votre credentials.")
        return self.instance.command()


    def remove(self) -> None:
        """
        → Logique associée à la commande 'remove'.
        :return: Rien
        """
        keys = list(self.arguments["args"].keys()) or []
        try: id = int(keys[0])
        except (ValueError, IndexError):
            methods.console("bright_red", f"[✘] Erreur : Éxécution incorrecte de la commande, argument(s) manquant(s) ou incorrect : <id>")
            return self.instance.help("credentials", "remove")

        credential = Credentials(self.instance.app, id=id)
        if not credential.exists:
            methods.console("bright_red", "[✘] Erreur : Aucun credentials trouvé pour l'ID fourni.")
            return self.instance.command()
        if not credential.user_id == self.instance.app.user.id:
            methods.console("bright_red", "[✘] Erreur : Vous n'êtes pas autorisé à supprimer ce credentials.")
            return self.instance.command()

        if credential.delete(): methods.console("green", "[✔] Succès : Votre credentials a été supprimé avec succès.")
        else: methods.console("bright_red", "[✘] Erreur : Une erreur s'est produite lors de la suppression de votre credential.")
        return self.instance.command()


    def edit(self) -> None:
        """
        → Logique associée à la commande 'edit'.
        :return: Rien
        """
        keys = list(self.arguments["args"].keys()) or []
        try: id = int(keys[0])
        except (ValueError, IndexError):
            methods.console("bright_red", f"[✘] Erreur : Éxécution incorrecte de la commande, argument(s) manquant(s) ou incorrect : <id>")
            return self.instance.help("credentials", "edit")

        if not len(keys) > 1:
            methods.console("bright_red", "[✘] Erreur : Aucun argument à modifier n'a été fourni.")
            return self.instance.help("credentials", "edit")

        if not "password" in keys and ("encryption_key" in keys or "encryption_type" in keys):
            methods.console("bright_red", "[✘] Erreur : Vous ne pouvez pas modifier le type de chiffrement ou la clé de chiffrement sans modifier le mot de passe.")
            return self.instance.command()

        if "encryption_key" in keys and not "encryption_type" in keys:
            methods.console("bright_red", "[✘] Erreur : Vous ne pouvez pas modifier la clé de chiffrement sans modifier le type de chiffrement.")
            return self.instance.command()

        labels = self.arguments["args"].get("label", None)
        if labels is not None:
            if not isinstance(labels, list): labels = [labels]
            labels = [label.lower() for label in labels] if labels else []

        credential = Credentials(self.instance.app, id=id)
        if not credential.exists:
            methods.console("bright_red", "[✘] Erreur : Aucun credentials trouvé pour l'ID fourni.")
            return self.instance.command()
        if not credential.user_id == self.instance.app.user.id:
            methods.console("bright_red", "[✘] Erreur : Vous n'êtes pas autorisé à modifier ce credentials.")
            return self.instance.command()

        data = {
            "website": self.arguments["args"].get("website", None),
            "login": self.arguments["args"].get("login", None),
            "password": self.arguments["args"].get("password", None),
            "encryption_type": self.arguments["args"].get("encryption_type", None),
            "encryption_key": self.arguments["args"].get("encryption_key", None),
            "labels": labels
        }

        if credential.update(**data): methods.console("green", "[✔] Succès : Votre credentials a été modifié avec succès.")
        else: methods.console("bright_red", "[✘] Erreur : Une erreur s'est produite lors de la modification de votre credential.")
        return self.instance.command()


    def show(self) -> None:
        """
        → Logique associée à la commande 'show'.
        :param args: Dictionnaire contenant les arguments pour afficher l'entrée.
        :return: Rien
        """
        pass


    def list(self) -> None:
        """
        → Logique associée à la commande 'list'.
        :return: None
        """
        pass


    def generate(self) -> None:
        """
        → Logique associée à la commande 'generate'.
        :return: None
        """
        params = self.arguments["args"].keys()
        length, strength = None, None
        try: strength = int(self.arguments["args"].get("strength")) if self.arguments["args"].get("strength") else 3
        except ValueError:  methods.console("yellow", "[ί] Attention : La force doit être comprise en 1 et 4. Utilisation de la force par défaut.")

        try: length = int(self.arguments["args"].get("length")) if self.arguments["args"].get("length") else 12
        except ValueError: methods.console("yellow", "[ί] Attention : La longueur doit être un nombre entier. Utilisation de la longueur par défaut.")

        data = {
            "length": length,
            "use_mixed_case": not "no_mixed_case" in params,
            "use_numbers": not "no_numbers" in params,
            "use_specials": not "no_specials" in params,
            "use_dictionary": "use_dictionary" in params,
            "strength": strength
        }

        success, response = generate_password(**data)
        if not success: methods.console("bright_red", f"[✘] Erreur : {response}"); return self.instance.command()
        methods.console("green", "[✔] Succès : Mot de passe généré avec succès, pensez à le sauvegarder !")
        ui.secure_print(response)
        return self.instance.command()

    def audit(self) -> None:
        """
        → Logique associée à la commande 'audit'.
        :return: None
        """
        pass
