class Credentials:
    def __init__(self, database):
        self.database = database
        self.user = self.database.user
        self.data = self.database.complete["credentials"]

    def get_by_id(self, id: int):
        request = self.database.get("credentials", "id", id)
        return request

    def get_by_name(self, name):
        request = self.database.get("utilisateur", "username", name)
        return request

    def exists(self, name):
        request = self.database.get("utilisateur", "username", name)
        return request is not None

    def create(self, website, login, password:Password, encryption_type, encryption_key: str = ""):
        new = {
            "id": 1,
            "user_id": self.user.id,
            "website": website,
            "login": login,
            "password": password.encrypted,
            "strength": 4,
            "is_expired": False,
            "encryption_type": encryption_type,  # AES, RSA, CESAR
            "encryption_key": encryption_key,  # AES: Salt
        },
        return self.database.add("credentials", user)

    def get_rsa_keys(self, id: int):
        request = self.database.get("utilisateur", "id", id)
        return request["rsa_public_key"], request["rsa_private_key"]