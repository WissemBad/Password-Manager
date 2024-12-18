import os
import json

from utils import configuration as configuration

from database import user, credentials

match configuration.database_mode:

    case 0: # DATABASE MODE : JSON
        class Database:
            database_location = "database/_data/database.json"
            template = configuration.template["database"]
            
            def __init__(self, app):
                self.app = app
                self.complete = self.load()

                self.user = user.User(self)
                self.credentials = credentials.DataCredentials(self)
                self.label = None

            def generate(self):
                """→ Générer la base de données."""
                with open(self.database_location, "w", encoding="utf-8") as file:
                    json.dump(self.template, file, indent=4, ensure_ascii=False)
                return self.load()

            def load(self):
                """→ Charger la base de données."""
                if not os.path.exists(self.database_location): return self.generate()
                with open(self.database_location, "r", encoding="utf-8") as file:
                    database = json.load(file)
                return database

            def save(self):
                """→ Sauvegarder la base de données."""
                with open(self.database_location, "w", encoding="utf-8") as file:
                    json.dump(self.complete, file, indent=4, ensure_ascii=False)
                return True

            def add(self, location:str, data:dict):
                """→ Ajouter un élément à la base de données."""
                if not location in self.complete:
                    raise Exception(f"[✘] Erreur : [location:{location}] n'existe pas dans la base de données.")

                self.complete[location].append(data)
                return self.save()

            def find_id(self, location: str, thing: str, data):
                """→ Trouver l'ID d'un élément dans la base de données."""
                if not location in self.complete:
                    raise Exception(f"[✘] Erreur : [location:{location}] n'existe pas dans la base de données.")

                for element in self.complete[location]:
                    if element[thing] == data:
                        return element["id"]
                return None

            def get(self, location: str, search: str, data):
                """→ Récupérer un élément de la base de données."""
                if not location in self.complete:
                    raise Exception(f"[✘] Erreur : [location:{location}] n'existe pas dans la base de données.")

                for element in self.complete[location]:
                    if element[search] == data: return element
                return None

            # - Modifier un élément de la base de données
            def update(self, location: str, search: str, data, thing:str, push):
                """→ Modifier un élément de la base de données."""
                if not location in self.complete:
                    raise Exception(f"[✘] Erreur : [location:{location}] n'existe pas dans la base de données.")

                for element in self.complete[location]:
                    if element[search] == data:
                        element[thing] = push
                        return self.save()
                return None

            def delete(self, location:str, search: str, data):
                """→ Supprimer un élément de la base de données."""
                if not location in self.complete:
                    raise Exception(f"[✘] Erreur : [location:{location}] n'existe pas dans la base de données.")

                for element in self.complete[location]:
                    if element[search] == data:
                        self.complete[location].remove(element)
                        return self.save()
                return None
    case 1:
        raise Exception("[!] Le mode [Database:SQL] n'est pas encore implémenté.")

