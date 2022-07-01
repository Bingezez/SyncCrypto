from lib.database.client_db import RegisterNewClient

name_db = 'client.db'
path_data = './server/database/'


class LookDb:
    def __init__(self):
        self._db = RegisterNewClient(name_db, path_data)

    def get_all(self):
        return self._db.get_all_clients()
    

if __name__ == '__main__':
    db = LookDb()
    print(db.get_all())
