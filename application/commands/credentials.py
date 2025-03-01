import time

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
            case "history": self.history()
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

        labels = self.arguments["args"].get("labels", [])
        if not isinstance(labels, list): labels = [labels]
        labels = [label.lower() for label in labels] if labels else []
        encryption_key = None
        try: encryption_key = int(self.arguments["args"].get("cesar_key")) if self.arguments["args"].get("cesar_key") else None
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

        labels = self.arguments["args"].get("labels", None)
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

        encryption_key = self.arguments["args"].get("encryption_key", None)

        data = {
            "website": self.arguments["args"].get("website", None),
            "login": self.arguments["args"].get("login", None),
            "password": self.arguments["args"].get("password", None),
            "encryption_type": self.arguments["args"].get("encryption_type", None),
            "encryption_key": None,
            "labels": labels
        }

        if encryption_key is not None: data["encryption_key"] = int(encryption_key)
        if credential.update(**data): methods.console("green", "[✔] Succès : Votre credentials a été modifié avec succès.")
        else: methods.console("bright_red", "[✘] Erreur : Une erreur s'est produite lors de la modification de votre credential.")
        return self.instance.command()


    def show(self) -> None:
        """
        → Logique associée à la commande 'show'.
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

        crypt = not "decrypted" in keys
        if credential.show(crypt): methods.console("green", "[✔] Succès : Détails du credentials affichés avec succès.")
        else: methods.console("bright_red", "[✘] Erreur : Une erreur s'est produite lors de l'affichage des détails de votre credential.")
        return self.instance.command()

    def list(self) -> None:
        """
        → Logique associée à la commande 'list'.
        :return: None
        """
        params = self.arguments["args"]
        allowed_params = ["website", "login", "labels", "strength", "encryption_type"]  # Paramètres autorisés pour la recherche
        user_credentials = self.instance.app.database.credentials.get_user_credentials(self.instance.app.user.id)
        response = []

        # Liste des paramètres non autorisés
        invalid_params = [key for key in params.keys() if key not in allowed_params]

        if invalid_params:
            for param in invalid_params:
                methods.console("yellow", f"[ί] Avertissement : Le paramètre '{param}' n'est pas supporté. Il sera ignoré.")
            params = {key: value for key, value in params.items() if key in allowed_params}

        # Affichage de la recherche avec critères
        if params:
            criteria_display = " | ".join([f"{key}={value}" for key, value in params.items()])
            methods.console("blue", f"[ί] Note : Recherche avancée avec des critères : {criteria_display}")
        else: methods.console("blue", "[ί] Note : Affichage de toutes les entrées...")
        time.sleep(1.5)

        for credential in user_credentials:
            matches_labels = True
            labels = self.arguments["args"].get("labels", None)

            if labels is not None:
                if not isinstance(labels, list):
                    labels = [labels]
                search_labels = [label.lower() for label in labels] if labels else []
                matches_labels = all(label in credential.get("labels", []) for label in search_labels)
            matches_criteria = all(credential.get(key) == value for key, value in params.items() if key != "labels")

            if matches_criteria and matches_labels:
                credential = Credentials(self.instance.app, credential["id"])
                response.append(credential)

        if response:
            for cred in response: cred.list_show()
            methods.console("green", f"[✔] Succès : {len(response)} résultat(s) trouvé(s).")
        else: methods.console("bright_red", "[✘] Échec : Aucun résultat n'a été trouvé avec vos critères.")
        return self.instance.command()

    def generate(self) -> None:
        """
        → Logique associée à la commande 'generate'.
        :return: None
        """
        params = list(self.arguments["args"].keys())
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
        :return: Rien
        """
        keys = list(self.arguments["args"].keys()) or []
        try: id = int(keys[0])
        except (ValueError, IndexError):
            methods.console("bright_red", f"[✘] Erreur : Éxécution incorrecte de la commande, argument(s) manquant(s) ou incorrect : <id>")
            return self.instance.help("credentials", "audit")


        credential = Credentials(self.instance.app, id=id)
        if not credential.exists:
            methods.console("bright_red", "[✘] Erreur : Aucun credentials trouvé pour l'ID fourni.")
            return self.instance.command()
        if not credential.user_id == self.instance.app.user.id:
            methods.console("bright_red", "[✘] Erreur : Vous n'êtes pas autorisé à consulter ce credentials.")
            return self.instance.command()

        credential.audit(); return self.instance.command()

    def history(self) -> None:
        """
        → Logique associée à la commande 'audit'.
        :return: Rien
        """
        keys = list(self.arguments["args"].keys()) or []

        try: id = int(keys[0])
        except (ValueError, IndexError):
            methods.console("bright_red", f"[✘] Erreur : Éxécution incorrecte de la commande, argument(s) manquant(s) ou incorrect : <id>")
            return self.instance.help("credentials", "history")

        try: ID = int(self.arguments["args"][keys[0]])
        except (ValueError, IndexError):
            methods.console("bright_red", f"[✘] Erreur : Éxécution incorrecte de la commande, argument(s) manquant(s) ou incorrect : <history_id>")
            return self.instance.help("credentials", "history")

        credential = Credentials(self.instance.app, id=id)
        if not credential.exists:
            methods.console("bright_red", "[✘] Erreur : Aucun credentials trouvé pour l'ID fourni.")
            return self.instance.command()
        if not credential.user_id == self.instance.app.user.id:
            methods.console("bright_red", "[✘] Erreur : Vous n'êtes pas autorisé à consulter ce credentials.")
            return self.instance.command()
        try: exists = credential.history[ID]
        except IndexError:
            methods.console("bright_red", "[✘] Erreur : Aucun historique trouvé pour l'ID fourni.")
            return self.instance.command()

        crypt = not "decrypted" in keys
        credential.show_history(ID, crypt)
        return self.instance.command()