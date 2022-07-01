import time

from lib.stream import GlobalStreamData
from lib.utils import hash_string_sha224, create_folder

from threading import Thread

path_data = './server/data/'


class Registration(GlobalStreamData, Thread):
    def __init__(self, reader, writer, db):
        super(Registration, self).__init__(reader, writer)
        Thread.__init__(self)
        self._db = db

    async def registration(self, data):
        username = data['username']
        password = data['password']
        path_user = hash_string_sha224(username + str(time.time()))
        self.action = 'registation'
        if self._db.get_client_by_username(username):
            self.status = 'error'
            self.message = 'Username already exist'
        else:
            self._db.add_client(
                [None,
                 username,
                 password,
                 path_user,
                 None]
            )
            self.status = 'success'
            self.message = 'Registration success'
            await create_folder(path_data + '/' + path_user)
        await self.transfer_data()
