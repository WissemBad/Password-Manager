class User:
    def __init__(self, database):
        self.database = database
        self.data = self.database.complete["utilisateur"]

    def get_by_id(self, id:int):
        request = self.database.get("utilisateur", "id", id)
        return request

    def get_by_name(self, name):
        request = self.database.get("utilisateur", "username", name)
        return request

    def exists(self, name):
        request = self.database.get("utilisateur", "username", name)
        return request is not None

    def create(self, user):
        return self.database.add(user)