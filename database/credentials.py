from application.credentials import Credentials
from utils import methods


class DataCredentials:
    def __init__(self, database) -> None:
        self.database = database
        self.user = self.database.app.user
        self.data: list[dict] = self.database.complete["credentials"]
        self.user_credentials: list[dict] = self.get_user_credentials(self.user.id)


    def exists(self, id: int) -> bool:
        """
        → Vérifier si des données existent dans la base de données.
        :param id: L'identifiant des données à vérifier.
        :return: True si les données existent, False sinon.
        """
        return self.database.get("credentials", "id", id) is not None


    def get_by_id(self, id: int) -> dict | None:
        """
        → Récupérer des données par ID.
        :param id: L'identifiant des données à récupérer.
        :return: Un dictionnaire contenant les données, ou None si non trouvé.
        """
        return self.database.get("credentials", "id", id)


    def delete(self, id: int) -> bool:
        """
        → Supprimer des données de la base de données.
        :param id: L'identifiant des données à supprimer.
        :return: True si la suppression a réussi, False sinon.
        """
        return self.database.delete("credentials", "id", id)


    def get_user_credentials(self, user_id: int) -> list[dict]:
        """
        → Récupérer les données d'un utilisateur.
        :param user_id: L'identifiant de l'utilisateur.
        :return: Une liste de dictionnaires contenant les données de l'utilisateur.
        """
        response: list[dict] = []
        for element in self.data:
            if element["user_id"] == user_id:
                response.append(element)
        return response


    def update(self, credentials: Credentials) -> bool:
        """
        → Mettre à jour des données dans la base de données.
        :param credentials: Les informations d'identification à mettre à jour.
        :return: True si la mise à jour a réussi, False sinon.
        """
        data: dict = {
            "id": credentials.id,
            "user_id": credentials.user_id,
            "website": credentials.website,
            "login": credentials.login,
            "password": credentials.password.encrypted,
            "strength": credentials.password.strength,
            "encryption_type": credentials.password.encryption_type,
            "encryption_key": credentials.password.encryption_key,
            "labels": credentials.labels,
            "updated_at": methods.get_current_time(),
            "created_at": credentials.created_at,
            "history": credentials.history,
        }

        for element in self.data:
            if element["id"] == credentials.id:
                old: dict = element.copy()
                element.update(data)
                if not old["password"] == element["password"] or \
                   not old["strength"] == element["strength"] or \
                   not old["encryption_type"] == element["encryption_type"] or \
                   not old["encryption_key"] == element["encryption_key"] or \
                   not old["website"] == element["website"] or \
                   not old["login"] == element["login"]:
                    element["history"].insert(0, generate_history(old))
                return self.database.save()
        return False


    def create(self, credentials: Credentials) -> bool:
        """
        → Ajouter des données à la base de données.
        :param credentials: Les informations d'identification à ajouter.
        :return: True si l'ajout a réussi, False sinon.
        """
        data: dict = {
            "id": credentials.id,
            "user_id": credentials.user_id,
            "website": credentials.website,
            "login": credentials.login,
            "password": credentials.password.encrypted,
            "strength": credentials.password.strength,
            "encryption_type": credentials.password.encryption_type,
            "encryption_key": credentials.password.encryption_key,
            "labels": credentials.labels,
            "updated_at": methods.get_current_time(),
            "created_at": methods.get_current_time(),
            "history": [],
        }
        return self.database.add("credentials", data)


def generate_history(data: dict) -> dict:
    """
    → Générer l'historique des mots de passe.
    :param data: Les données à inclure dans l'historique.
    :return: Un dictionnaire contenant l'historique des mots de passe.
    """
    return {
        "website": data["website"],
        "login": data["login"],
        "password": data["password"],
        "strength": data["strength"],
        "encryption_type": data["encryption_type"],
        "encryption_key": data["encryption_key"],
        "updated_at": data["updated_at"],
    }
