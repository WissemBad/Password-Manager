from application.user import User

class DataUser:
    def __init__(self, database) -> None:
        self.database = database
        self.data: list[dict] = self.database.complete["utilisateur"]


    def get_by_id(self, user_id: int) -> dict | None:
        """
        → Récupérer les données d'un utilisateur à partir de l'ID.
        :param user_id: L'ID de l'utilisateur à rechercher.
        :return: Les données de l'utilisateur si trouvé, None sinon.
        """
        request = self.database.get("utilisateur", "id", user_id)
        return request


    def get_by_name(self, name: str) -> dict | None:
        """
        → Récupérer les données d'un utilisateur à partir du nom d'utilisateur.
        :param name: Le nom d'utilisateur à rechercher.
        :return: Les données de l'utilisateur si trouvé, None sinon.
        """
        request = self.database.get("utilisateur", "username", name)
        return request


    def exists(self, name: str) -> bool:
        """
        → Vérifier si un utilisateur existe.
        :param name: Le nom d'utilisateur à vérifier.
        :return: True si l'utilisateur existe, False sinon.
        """
        request = self.database.get("utilisateur", "username", name)
        return request is not None


    def create(self, user: User) -> bool:
        """
        → Ajouter un utilisateur à la base de données.
        :param user: L'objet User à ajouter.
        :return: True si l'ajout a réussi, False sinon.
        """
        data = {
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "rsa_public_key": user.rsa_public_key,
            "rsa_private_key": user.rsa_private_key
        }
        return self.database.add("utilisateur", data)


    def get_encryption_keys(self, user_id: int) -> tuple[str, str]:
        """
        → Récupérer les clés de chiffrement RSA d'un utilisateur.
        :param user_id: L'ID de l'utilisateur.
        :return: Un tuple contenant la clé publique et la clé privée de l'utilisateur.
        """
        request = self.database.get("utilisateur", "id", user_id)
        return request["rsa_public_key"], request["rsa_private_key"]

    def delete(self, id):
        pass
