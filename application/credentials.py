from typing import Optional

from application.main import Application
from application.password import Password
from application.user import User
from database.main import Database


class Credentials:
    def __init__(self, app: Application, id: int, website: Optional[str] = None, login: Optional[str] = None, password: Optional[str] = None, encryption_type: Optional[str] = None, encryption_key: Optional[str] = None, labels: Optional[list] = None):
        self.app:Application = app
        self.database: Database = self.app.database
        self.user: User = self.app.user

        self.id: int = id
        self.exists: bool = self.database.credentials.exists(self.id)

        if self.exists:
            self.data = self.database.credentials.get_by_id(self.id)
            self.website = self.data["website"]
            self.login = self.data["login"]
            self.labels = self.data["labels"]
            self.password = Password(crypt=False, password=self.data["password"], encryption_type=self.data["encryption_type"], app=self.app, encryption_key=self.data["encryption_key"])
            self.history = self.data["history"]
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
                elif encryption_type is not None: self.password = Password(True, password, encryption_type, self.app, self.password.encryption_key)
                else: self.password = Password(True, password, self.password.encryption_type, self.app, self.password.encryption_key)
            else: self.password = self.password
            return self.database.credentials.update(self)
        except Exception as error:
            print(f"[✘] Erreur lors de la mise à jour des credentials : {error}")
            return False