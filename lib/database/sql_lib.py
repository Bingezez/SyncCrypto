import sqlite3

from sqlite3 import Error
from os import path, makedirs


class Sql:
    def __init__(self, name_database, path_database=None):
        self.path_database = path_database or '.'

        if not path.exists(self.path_database):
            makedirs(self.path_database)

        try:
            self._connection = sqlite3.connect(path.join(
                self.path_database, name_database))
            self._cursor = self._connection.cursor()
        except Error as e:
            print(f'Error {e}: In the database: {name_database}.')

    def execute(self, sql, params=None):
        self._cursor.execute(sql, params or ())

    def executemany(self, sql, param_list):
        self._cursor.executemany(sql, param_list)

    def query(self, sql, params=None):
        self._cursor.execute(sql, params or ())
        return self._cursor.fetchall()

    def commit(self):
        self._connection.commit()

    def close(self):
        self._connection.close()
