from lib.stream import GlobalStreamData

from Interface.client.login import Login
from Interface.client.token import Token
from Interface.client.registration import Registration

from Interface.client.note import CreateNewNote, \
    Note, SyncNotes


class Interface(GlobalStreamData):
    def __init__(self, reader, writer):
        GlobalStreamData.__init__(self, reader, writer)
        self._token = None

    async def print_menu(self):
        print('[1]. Login to server\n'
              '[2]. Register new client\n'
              '[3]. Exit\n')

    async def print_menu_user(self):
        print('[1]. Create new note\n'
              '[2]. Action with note\n'  # read/edit/delete/show all notes
              '[3]. Sync notes \n'
              '[4]. Logout\n'
              '[5]. Exit\n')

    async def error_ops(self):
        print('Wrong action')
        await self.main()

    async def perform_ops_menu(self, choose_ops):
        ops = {'1': self.login,
               '2': self.registration,
               '3': self.close}
        await ops.get(choose_ops, self.error_ops)()

    async def perform_ops_menu_user(self, choose_ops):
        ops = {'1': self.new_note,
               '2': self.action_with_note,
               '3': self.sync_notes,
               '4': self.logout,
               '5': self.close}
        await ops.get(choose_ops, self.error_ops)()

    async def login(self):
        await Login(self.reader, self.writer).login()

    async def logout(self):
        await Login(self.reader, self.writer).logout()

    async def registration(self):
        await Registration(self.reader, self.writer) \
            .register()

    async def new_note(self):
        await CreateNewNote(self.reader, self.writer, self._token).new_note()

    async def action_with_note(self):
        await Note(self.reader, self.writer, self._token).main()

    async def sync_notes(self):
        await SyncNotes(self.reader, self.writer, self._token).main()

    async def save_token(self):
        token = Token(self.reader, self.writer)
        await token.save_token(self.data)
        self._token = await token.read_token()

    async def base_action(self):
        while True:
            await self.print_menu()

            act = input('Choose action: ')
            await self.perform_ops_menu(act)
            await self.read_data()

            if self.status == 'error':
                print(self.message)
                continue

            if self.status == 'success':
                print(self.message)

            if self.action == 'token':
                await self.save_token()
                break

    async def main(self):
        await self.base_action()
        while True:
            await self.print_menu_user()
            act = input('Choose action: ')
            await self.perform_ops_menu_user(act)
            
            await self.read_data()

            if self.action == 'logout':
                await self.logout()
                await self.base_action()

            if self.message is None:
                continue
            else:
                print(self.message)
