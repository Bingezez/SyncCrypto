from lib.stream import GlobalStreamData

from Interface.server.this_user import user

from Interface.server.login import Login
from Interface.server.registration import Registration
from Interface.server.note import CreateNewNote, \
 PathUser, Note, SyncNotes


class Interface(GlobalStreamData):
    def __init__(self, reader, writer, db):
        super(Interface, self).__init__(reader, writer)
        self._db = db

    async def login(self):
        login = Login(self.reader, self.writer, self._db)
        await login.login(self.data)
        return login.status
    
    async def logout(self):
        await Login(self.reader, self.writer, self._db).logout()

    async def registration(self):
        registration = Registration(self.reader, self.writer, self._db)
        await registration.registration(self.data)

    async def new_note(self, data):
        note = CreateNewNote(self.reader, self.writer)
        await note.new_note(data, user(data['token'])[3])

    async def get_all_notes(self, data):
        get = PathUser(self.reader, self.writer)
        await get.send(user(data['token'])[3])

    async def read_note(self, data):
        note = Note(self.reader, self.writer)
        await note.read_note(data, user(data['token'])[3])

    async def edit_note(self, data):
        note = Note(self.reader, self.writer)
        await note.edit_note(data, user(data['token'])[3])
    
    async def delete_note(self, data):
        note = Note(self.reader, self.writer)
        await note.delete_note(data, user(data['token'])[3])
    
    async def sync_notes(self, data):
        upload = SyncNotes(self.reader, self.writer)
        await upload.sync_notes(data, user(data['token'])[3])

    async def download_notes(self, data):
        download = SyncNotes(self.reader, self.writer)
        await download.download_notes(user(data['token'])[3])

    async def back_to_menu(self):
        self.action = 'back_to_menu'
        await self.transfer_data()

    async def auth_client(self):
        while True:
            await self.read_data()
            if self.action == 'login':
                if await self.login() == 'success':
                    break

            if self.action == 'registration':
                await self.registration()

    async def main(self):
        await self.auth_client()
        while True:
            await self.read_data()
            if self.action == 'logout':
                await self.logout()
                await self.auth_client()
            elif self.action == 'new_note':
                await self.new_note(self.data)
            elif self.action == 'get_all_notes':
                await self.get_all_notes(self.data)
            elif self.action == 'read_note':
                await self.read_note(self.data)
            elif self.action == 'edit_note':
                await self.edit_note(self.data)
            elif self.action == 'delete_note':
                await self.delete_note(self.data)
            elif self.action == 'upload_note':
                await self.sync_notes(self.data)
            elif self.action == 'download_notes':
                await self.download_notes(self.data)
            elif self.action == 'back_to_menu':
                await self.back_to_menu()
