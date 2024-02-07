from .sql_lib import Sql


class RegisterNewClient:
    '''
    id: int - autoincrement
    username: str - not null - client username
    password: str - not null - client password
    path: str - not null - path to client folder
    friend_list: str - not null - list of friends 
    '''

    _name_table = 'clients'
    _name_columns = '(id INTEGER PRIMARY KEY AUTOINCREMENT,' \
                    'username TEXT NOT NULL,' \
                    'password TEXT NOT NULL,' \
                    'path TEXT ,' \
                    'friend_list TEXT [this is list of friends])'

    def __init__(self, name_db, path_db=None):
        self._sql = Sql(name_db, path_db)

    def create_tbl(self):
        self._sql.execute(f'''CREATE TABLE IF NOT EXISTS
            {self._name_table} {self._name_columns}''')
        self._sql.commit()

    def add_client(self, row):
        self._sql.execute(f'''INSERT INTO {self._name_table}
                            VALUES(?,?,?,?,?)''', row)
        self._sql.commit()

    def get_client_by_username(self, username):
        try :
            return self._sql.query(f'''SELECT * FROM {self._name_table}
                            WHERE username = ?''', (username,))[0]
        except IndexError:
            pass
        
    def get_all_clients(self):
        return self._sql.query(f'''SELECT * FROM {self._name_table}''')


if __name__ == '__main__':
    pass
