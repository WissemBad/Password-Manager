import os
import json

from application.main import Application
from utils import configuration, methods

from database.user import DataUser
from database.credentials import DataCredentials

# - Mode [Database:JSON]
class Database:
    database_location: str = "database/_data/database.json"
    template: dict = configuration.template["database"]

    def __init__(self, app: Application) -> None:
        self.app: Application = app
        self.complete: dict = self.load()

        self.user: DataUser = DataUser(self)
        self.credentials: DataCredentials | None = None


    def init_dependencies(self) -> None:
        """ → Initialiser les dépendances de la base de données. """
        self.credentials = DataCredentials(self)


    def generate(self) -> dict:
        """
         → Générer la base de données.
        :return: Le contenu de la base de données générée.
        """
        directory = os.path.dirname(self.database_location)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(self.database_location, "w", encoding="utf-8") as file:
            json.dump(self.template, file, indent=4, ensure_ascii=False)
        return self.load()


    def load(self) -> dict:
        """
        → Charger la base de données.
        :return: Le contenu de la base de données chargée.
        """
        if not os.path.exists(self.database_location):
            return self.generate()
        with open(self.database_location, "r", encoding="utf-8") as file:
            database = json.load(file)
        return database


    def save(self) -> bool:
        """
        → Sauvegarder la base de données.
        :return: True si la sauvegarde a réussi, False sinon.
        """
        try:
            with open(self.database_location, "w", encoding="utf-8") as file:
                json.dump(self.complete, file, indent=4, ensure_ascii=False)
            return True
        except Exception as error:
            methods.console("red", f"[✘] Erreur : Enregistrement impossible de la base de données : {error}")
            return False


    def add(self, location: str, data: dict) -> bool:
        """
        → Ajouter un élément à la base de données.
        :param location: La section cible de la base de données.
        :param data: Les données à ajouter.
        :return: True si l'ajout a réussi, False sinon.
        """
        if location not in self.complete:
            raise Exception(f"[✘] Erreur : [location:{location}] n'existe pas dans la base de données.")

        self.complete[location].append(data)
        return self.save()


    def find_id(self, location: str, thing: str, data) -> int | None:
        """
        → Trouver l'ID d'un élément dans la base de données.
        :param location: La section cible de la base de données.
        :param thing: Le champ à chercher.
        :param data: La valeur recherchée.
        :return: L'ID de l'élément correspondant, ou None si non trouvé.
        """
        if location not in self.complete:
            raise Exception(f"[✘] Erreur : [location:{location}] n'existe pas dans la base de données.")

        for element in self.complete[location]:
            if element[thing] == data:
                return element["id"]
        return None


    def get(self, location: str, search: str, data) -> dict | None:
        """
        → Récupérer un élément de la base de données.
        :param location: La section cible de la base de données.
        :param search: Le champ à chercher.
        :param data: La valeur recherchée.
        :return: L'élément correspondant, ou None si non trouvé.
        """
        if location not in self.complete:
            raise Exception(f"[✘] Erreur : [location:{location}] n'existe pas dans la base de données.")

        for element in self.complete[location]:
            if element[search] == data:
                return element
        return None


    def update(self, location: str, search: str, data, thing: str, push) -> bool | None:
        """
        → Modifier un élément de la base de données.
        :param location: La section cible de la base de données.
        :param search: Le champ à chercher.
        :param data: La valeur recherchée.
        :param thing: Le champ à modifier.
        :param push: La nouvelle valeur à appliquer.
        :return: True si la mise à jour a réussi, None sinon.
        """
        if location not in self.complete:
            raise Exception(f"[✘] Erreur : [location:{location}] n'existe pas dans la base de données.")

        for element in self.complete[location]:
            if element[search] == data:
                element[thing] = push
                return self.save()
        return None


    def delete(self, location: str, search: str, data) -> bool | None:
        """
        → Supprimer un élément de la base de données.
        :param location: La section cible de la base de données.
        :param search: Le champ à chercher.
        :param data: La valeur recherchée.
        :return: True si la suppression a réussi, None sinon.
        """
        if location not in self.complete:
            raise Exception(f"[✘] Erreur : [location:{location}] n'existe pas dans la base de données.")

        for element in self.complete[location]:
            if element[search] == data:
                self.complete[location].remove(element)
                return self.save()
        return None
