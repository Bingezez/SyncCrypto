import time

from os.path import join

from lib.stream import GlobalStreamData
from lib.utils import hash_string_sha224

session_file = 'session.txt'
path_session = './server/session/'


class Login(GlobalStreamData):
    def __init__(self, reader, writer, db):
        GlobalStreamData.__init__(self, reader, writer)
        self._db = db
        self._token = None

    async def create_token(self, data):
        username = data['username']
        self._token = hash_string_sha224(username + str(time.time()))
        line = f'{self._token}:{self._db.get_client_by_username(username)}'
        with open(join(path_session, session_file), 'a') as f:
            f.write(line + '\n')

    async def login(self, data):
        username = data['username']
        password = data['password']
        self.action = 'token'
        self.message = ''
        try:
            if self._db.get_client_by_username(username)[2] == password:
                self.status = 'success'
                self.message = f'Login success {username}'
        except IndexError:
            self.status = 'error'
            self.message = 'Username is not exist!'

        await self.create_token(data)
        self.data = {'token': self._token}
        await self.transfer_data()
    
    async def logout(self):
        self.action = 'logout'
        await self.transfer_data()
