from application.credentials import Credentials
from utils import methods


class DataCredentials:
    def __init__(self, database):
        self.database = database
        self.user = self.database.app.user

        self.data = self.database.complete["credentials"]
        self.dataCredentials = self.get_user_credentials(self.user.id)

    def exists(self, id: int):
        """→ Vérifier si des données existent."""
        return self.database.get("credentials", "id", id) is not None

    def get_by_id(self, id: int):
        """→ Récupérer des données par ID."""
        return self.database.get("credentials", "id", id)

    def delete(self, id: int):
        """→ Supprimer des données de la base de données."""
        return self.database.delete("credentials", "id", id)

    def get_user_credentials(self, user_id: int):
        """→ Récupérer les données d'un utilisateur."""
        response = []
        for element in self.data:
            if element["user_id"] == user_id: response.append(element)
        return response

    def edit(self, id: int, data: dict):
        """→ Modifier des données dans la base de données."""
        for element in self.data:
            if element["id"] == id:
                element.update(data)
                element["history"].insert(0, generate_history(data))
                return self.database.save()
        return False

    def create(self, credentials:Credentials):
        """→ Ajouter des données à la base de données."""
        data = {
            "id": credentials.id,
            "user_id": credentials.user_id,
            "website": credentials.website,
            "login": credentials.login,
            "password": credentials.password.encrypted,
            "strength": credentials.password.strength,
            "encryption_type": credentials.password.encryption_type,    # (AES, RSA, CESAR)
            "encryption_key": credentials.password.encryption_key, # (AES: Salt, CESAR: Key)
            "labels": credentials.labels,
            "created_at": methods.get_current_time(),
            "history": []
        }
        return self.database.add("credentials", data)


def generate_history(data):
    """→ Générer l'historique des mots de passe."""
    return {
        "website": data["website"],
        "login": data["login"],
        "password": data["password"],
        "strength": data["strength"],
        "encryption_type": data["encryption_type"],
        "encryption_key": data["encryption_key"],
        "created_at": data["created_at"]
    }
