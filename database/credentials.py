from app.credentials import Credentials


class DataCredentials:
    def __init__(self, database):
        self.database = database
        self.user = self.database.app.user

        self.data = self.database.complete["credentials"]
        self.user_data = self.get_user_credentials(self.user.id)

    def get_user_credentials(self, user_id: int):
        """→ Récupérer les données d'un utilisateur."""
        response = []
        for element in self.data:
            if element["user_id"] == user_id: response.append(element)
        return response

    def get_by_website(self, website: str):
        """→ Récupérer des données par leur identifiant."""
        for element in self.data:
            if element["website"] == website: return element
        return None

    def exists(self, name):
        request = self.database.get("utilisateur", "username", name)
        return request is not None

    def create(self, credentials:Credentials):
        data = {
            "id": 1,
            "user_id": credentials.user_id,
            "website": credentials.website,
            "login": credentials.login,
            "password": credentials.password.encrypted,
            "strength": credentials.password.strength,
            "encryption_type": credentials.password.encryption_type,    # (AES, RSA, CESAR)
            "encryption_key": credentials.password.encryption_key,      # (AES: Salt)
            "is_expired": False
        },
        return self.database.add("credentials", data)