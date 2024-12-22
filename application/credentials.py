import base64
from typing import Optional

from application.password import Password
from application.user import User
from utils import methods


class Credentials:
    def __init__(self, app, id: int, website: Optional[str] = None, login: Optional[str] = None, password: Optional[str] = None, encryption_type: Optional[str] = None, encryption_key: Optional[str] = None, labels: Optional[list] = None):
        self.app = app
        self.database = self.app.database
        self.user: User = self.app.user

        self.id: int = id
        self.exists: bool = self.database.credentials.exists(self.id)

        if self.exists:
            self.data = self.database.credentials.get_by_id(self.id)
            self.website = self.data["website"]
            self.login = self.data["login"]
            self.labels = self.data["labels"]

            self.encryption_key = self.data["encryption_key"]
            self.encryption_type = self.data["encryption_type"]
            if self.encryption_type == "CESAR":
                if self.encryption_key is not None: self.encryption_key = int.from_bytes(self.app.security.manager.double_decrypt(base64.b64decode(self.encryption_key.encode("utf-8")), self.app.user.aes_encryption_key), byteorder='big')
                else: self.encryption_key = None
            self.password = Password(crypt=False, password=self.data["password"], encryption_type=self.encryption_type, app=self.app, encryption_key=self.encryption_key)
            self.history = self.data["history"]
            self.updated_at = self.data["updated_at"]
            self.created_at = self.data["created_at"]
            self.user_id = self.data["user_id"]

        elif website and login and password and encryption_type:
            self.website: str = website
            self.login: str = login
            self.password = Password(crypt=True, password=password, encryption_type=encryption_type, app=self.app, encryption_key=encryption_key)
            self.labels = labels
            self.user_id = self.user.id


    def create(self) -> bool:
        """
        → Ajouter une nouvelle entrée de mot de passe.
        :return: True si ajouté avec succès, False sinon.
        """
        return self.database.credentials.create(self)


    def delete(self) -> bool:
        """
        → Supprimer une entrée de mot de passe.
        :return: True si supprimé avec succès, False sinon.
        """
        if not self.exists or self.user_id != self.app.user.id: return False
        return self.database.credentials.delete(self.id)


    def update(self, website: Optional[str] = None, login: Optional[str] = None, password: Optional[str] = None, encryption_type: Optional[str] = None, encryption_key: Optional[str] = None, labels: Optional[list] = None) -> bool:
        """
        → Mettre à jour une entrée de mot de passe.
        :param website: Nouveau site (facultatif).
        :param login: Nouvel identifiant (facultatif).
        :param password: Nouveau mot de passe (facultatif).
        :param encryption_type: Nouveau type de chiffrement (facultatif).
        :param encryption_key: Nouvelle clé de chiffrement (facultatif).
        :param labels: Nouvelles étiquettes (facultatif).
        :return: True si mis à jour avec succès, False sinon.
        """
        if not self.exists or self.user_id != self.app.user.id: return False
        try:
            self.website = website if website is not None else self.website
            self.login = login if login is not None else self.login
            self.labels = labels if labels is not None else self.labels

            if password is not None:
                if encryption_key is not None and encryption_type is not None:  self.password = Password(True, password, encryption_type, self.app, encryption_key)
                elif encryption_key is not None: self.password = Password(crypt=True, password=password, encryption_type=self.password.encryption_type, app=self.app, encryption_key=encryption_key)
                elif encryption_type is not None:
                    if encryption_type == "CESAR": self.password = Password(True, password, encryption_type, self.app, self.encryption_key)
                    else: self.password = Password(True, password, encryption_type, self.app)
                else: self.password = Password(True, password, self.encryption_type, self.app, self.encryption_key)
            return self.database.credentials.update(self)
        except Exception as error:
            print(f"[✘] Erreur lors de la mise à jour des credentials : {error}")
            return False


    def show(self, crypt: bool = True) -> bool:
        """
        → Afficher les informations des credentials.
        :param crypt: Afficher le mot de passe chiffré.
        :return: True si affiché avec succès, False sinon.
        """
        try:
            labels = self.labels if self.labels else "Aucun"
            strength = {1: "Faible (1/4)", 2: "Moyen (2/4)", 3: "Fort (3/4)", 4: "Excellent (4/4)"}.get(self.password.strength, "Inconnu")

            col_width = 49  # Largeur générale de la colonne
            if crypt: password = "■■■■■■■■■■■■"
            else: password = self.password.decrypted

            def print_line(label, value):
                label_formatted = f"\033[1m{label}\033[0m"  # Gras
                value_formatted = f"\033[48;5;235m{str(value).rjust(col_width - len(label) - 3)}\033[0m"
                print(f"║ {label_formatted} : {value_formatted} ║")

            print("╔═══════════════════════════════════════════════════╗")
            print_line("• ID", self.id)
            print("║ ═════════════════════════════════════════════════ ║")
            print_line("• Site", self.website)
            print_line("• Identifiant", self.login)
            print_line("• Mot de passe", password)
            print_line("• Labels", labels)
            print("║ ═════════════════════════════════════════════════ ║")
            print_line("• Force", strength)
            print_line("• Chiffrement", self.password.encryption_type)
            print("║ ═════════════════════════════════════════════════ ║")
            print_line("• Date de création", self.created_at)
            print_line("• Dernière édition", self.updated_at)
            print_line("• Révisions",f"{len(self.history)} (IDs : {list(range(0, len(self.history)))})")
            print("╚═══════════════════════════════════════════════════╝")
            return True
        except Exception as error: print(f"[✘] Erreur lors de l'affichage des credentials : {error}"); return False


    def list_show(self) -> bool:
        """
        → Afficher les informations des credentials.
        :return: True si affiché avec succès, False sinon.
        """
        try:
            labels = self.labels if self.labels else "Aucun"
            col_width = 49  # Largeur générale de la colonne

            def print_line(label, value):
                label_formatted = f"\033[1m{label}\033[0m"  # Gras
                value_formatted = f"\033[48;5;235m{str(value).rjust(col_width - len(label) - 3)}\033[0m"
                print(f"║ {label_formatted} : {value_formatted} ║")

            print("╔═══════════════════════════════════════════════════╗")
            print_line("• ID", self.id)
            print("║ ═════════════════════════════════════════════════ ║")
            print_line("• Site", self.website)
            print_line("• Identifiant", self.login)
            print_line("• Labels", labels)
            print_line("• Dernière édition", self.updated_at)
            print("╚═══════════════════════════════════════════════════╝")
            return True
        except Exception as error: print(f"[✘] Erreur lors de l'affichage des credentials : {error}"); return False


    def audit(self):
        """
        → Analyser les failles de sécurité des credentials.
        :return: True si analysé avec succès, False sinon.
        """
        try:
            methods.password_audit(self.password.decrypted)
            return True
        except:  return False


    def show_history(self, ID: int, crypt: bool = True) -> bool:
        """
        → Afficher l'historique des modifications des credentials.
        :return: True si affiché avec succès, False sinon.
        """
        try:
            strength = {1: "Faible (1/4)", 2: "Moyen (2/4)", 3: "Fort (3/4)", 4: "Excellent (4/4)"}.get(self.history[ID]["strength"], "Inconnu")
            col_width = 49
            if crypt:
                password = "■■■■■■■■■■■■"
            else:
                encryption_key = self.history[ID]["encryption_key"]
                encryption_type = self.history[ID]["encryption_type"]
                if encryption_type == "CESAR":
                    if encryption_key is not None: encryption_key = int.from_bytes(self.app.security.manager.double_decrypt(base64.b64decode(encryption_key.encode("utf-8")), self.app.user.aes_encryption_key), byteorder='big')
                    else: self.encryption_key = None
                password = Password(crypt=False, password=self.data["password"], encryption_type=encryption_type, app=self.app, encryption_key=encryption_key)
                password = password.decrypted

            def print_line(label, value):
                label_formatted = f"\033[1m{label}\033[0m"  # Gras
                value_formatted = f"\033[48;5;235m{str(value).rjust(col_width - len(label) - 3)}\033[0m"
                print(f"║ {label_formatted} : {value_formatted} ║")

            print("╔═══════════════════════════════════════════════════╗")
            print_line("• ID", self.id)
            print_line("• Révision n°", ID)
            print_line("• Date de révision", self.history[ID]["updated_at"])
            print("║ ═════════════════════════════════════════════════ ║")
            print_line("• Site", self.history[ID]["website"])
            print_line("• Identifiant", self.history[ID]["login"])
            print_line("• Mot de passe", password)
            print("║ ═════════════════════════════════════════════════ ║")
            print_line("• Force", strength)
            print_line("• Chiffrement", self.history[ID]["encryption_type"])
            print("╚═══════════════════════════════════════════════════╝")
            return True
        except Exception as error:
            print(f"[✘] Erreur lors de l'affichage des credentials : {error}"); return False
