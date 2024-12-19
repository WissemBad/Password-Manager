from application.user import User

class DataUser:
    def __init__(self, database):
        self.database = database
        self.data = self.database.complete["utilisateur"]

    def get_by_id(self, user_id:int):
        """→ Récupérer les données d'un utilisateur à partir de l'ID."""
        request = self.database.get("utilisateur", "id", user_id)
        return request

    def get_by_name(self, name):
        """→ Récupérer les données d'un utilisateur à partir du nom d'utilisateur."""
        request = self.database.get("utilisateur", "username", name)
        return request

    def exists(self, name):
        """→ Vérifier si un utilisateur existe."""
        request = self.database.get("utilisateur", "username", name)
        return request is not None

    def create(self, user:User):
        """→ Ajouter un utilisateur à la base de données."""
        data = {
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "rsa_public_key": user.rsa_public_key,
            "rsa_private_key": user.rsa_private_key
        }
        return self.database.add("utilisateur", data)

    def get_encryption_keys(self, user_id:int):
        """→ Récupérer les clés de chiffrement RSA d'un utilisateur."""
        request = self.database.get("utilisateur", "id", user_id)
        return request["rsa_public_key"], request["rsa_private_key"]

