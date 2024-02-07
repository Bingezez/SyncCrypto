from getpass import getpass

from lib.stream import GlobalStreamData


class Login(GlobalStreamData):
    def __init__(self, reader, writer):
        super(Login, self).__init__(reader, writer)

    async def login(self):
        username = input('Username: ')
        password = getpass('Password: ')
        self.data = {'username': username,
                     'password': password}
        self.action = 'login'
        await self.transfer_data()
    
    async def logout(self):
        self.action = 'logout'
        await self.transfer_data()
