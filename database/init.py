import os
import json

from app import _config as configuration

class Database:
    def __init__(self):
        self.template = configuration.template["database"]
        self.complete = self.load()

        self.utilisateur = self.complete["utilisateur"]
        self.credentials = self.complete["credentials"]
        self.label = self.complete["label"]

    # Créer la base de données
    def generate(self):
        with open("database/_data/database.json", "w", encoding="utf-8") as file:
            json.dump(self.template, file, indent=4, ensure_ascii=False)
        return self.load()

    # Charger la base de données
    def load(self):
        if not os.path.exists("database/_data/database.json"): return self.generate()
        with open("database/_data/database.json", "r", encoding="utf-8") as file:
            database = json.load(file)
        return database

    # Sauvegarder la base de données
    def save(self):
        with open("database/_data/database.json", "w", encoding="utf-8") as file:
            json.dump(self.complete, file, indent=4, ensure_ascii=False)
        return True

    # - Ajouter un élément à la base de données
    def add(self, location:str, data:dict):
        if not location in self.complete:
            raise Exception(f"[location:{location}] n'existe pas dans la base de données.")

        self.complete[location].append(data)
        return self.save()

    # - Ajouter un élément à la base de données
    def find_id(self, location: str, thing: str, data):
        if not location in self.complete:
            raise Exception(f"[location:{location}] n'existe pas dans la base de données.")

        for element in self.complete[location]:
            if element[thing] == data:
                return element["id"]
        return None

    # - Récupérer un élément de la base de données
    def get_by_id(self, location:str, index:int):
        if not location in self.complete:
            raise Exception(f"[location:{location}] n'existe pas dans la base de données.")

        for element in self.complete[location]:
            if element["id"] == index: return element
        return None

    # - Modifier un élément de la base de données
    def update_by_id(self, location: str, index:int, thing:str, data):
        if not location in self.complete:
            raise Exception(f"[location:{location}] n'existe pas dans la base de données.")

        for element in self.complete[location]:
            if element["id"] == index:
                element[thing] = data
                return self.save()
        return None

    # - Supprimer un élément de la base de données
    def delete_by_id(self, location:str, index:int):
        if not location in self.complete:
            raise Exception(f"[location:{location}] n'existe pas dans la base de données.")

        for element in self.complete[location]:
            if element["id"] == index:
                self.complete[location].remove(element)
                return self.save()
        return None
