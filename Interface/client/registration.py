from getpass import getpass

from lib.stream import GlobalStreamData


class Registration(GlobalStreamData):
    def __init__(self, reader, writer):
        super(Registration, self).__init__(reader, writer)

    async def register(self):
        username = input('Username: ')
        while True:
            password = getpass('Password: ')
            if password == getpass('Repeat password: '):
                break
            print('Password not match')

        self.data = {'username': username,
                     'password': password}
        self.action = 'registration'
        await self.transfer_data()
