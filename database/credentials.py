class Credentials:
    def __init__(self, database):
        self.database = database
        self.data = self.database.complete["credentials"]

    def get_by_id(self, id):
        return
    def get_by_name(self, name):
        return

    def exists(self, name):
        return
    def create(self):
        return

    def update_by_id(self):
        return