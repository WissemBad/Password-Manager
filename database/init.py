import os
import json

from utils import _config as configuration

match configuration.database:

    case 0: # DATABASE MODE : JSON
        class Database:
            def __init__(self, app):
                self.app = app

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
                    raise Exception(f"[✘] Erreur : [location:{location}] n'existe pas dans la base de données.")

                self.complete[location].append(data)
                return self.save()

            # - Ajouter un élément à la base de données
            def find_id(self, location: str, thing: str, data):
                if not location in self.complete:
                    raise Exception(f"[✘] Erreur : [location:{location}] n'existe pas dans la base de données.")

                for element in self.complete[location]:
                    if element[thing] == data:
                        return element["id"]
                return None

            # - Récupérer un élément de la base de données grâce à l'identifiant
            def get(self, location: str, search: str, data):
                if not location in self.complete:
                    raise Exception(f"[✘] Erreur : [location:{location}] n'existe pas dans la base de données.")

                for element in self.complete[location]:
                    if element[search] == data: return element
                return None

            # - Modifier un élément de la base de données
            def update(self, location: str, search: str, data, thing:str, push):
                if not location in self.complete:
                    raise Exception(f"[✘] Erreur : [location:{location}] n'existe pas dans la base de données.")

                for element in self.complete[location]:
                    if element[search] == data:
                        element[thing] = push
                        return self.save()
                return None

            # - Supprimer un élément de la base de données
            def delete(self, location:str, search: str, data):
                if not location in self.complete:
                    raise Exception(f"[✘] Erreur : [location:{location}] n'existe pas dans la base de données.")

                for element in self.complete[location]:
                    if element[search] == data:
                        self.complete[location].remove(element)
                        return self.save()
                return None
    case 1:
        raise Exception("[!] Le mode [Database:SQL] n'est pas encore implémenté.")

