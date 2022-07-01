from lib.stream import GlobalStreamData


class Registration(GlobalStreamData):
    def __init__(self, reader, writer):
        super(Registration, self).__init__(reader, writer)

    async def register(self):
        username = input('Username: ')
        while True:
            password = input('Password: ')
            if password == input('Confirm password: '):
                break
            print('Password not match')

        self.data = {'username': username,
                     'password': password}
        self.action = 'registation'
        await self.transfer_data()
