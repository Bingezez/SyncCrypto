import os

from os import walk
from os.path import join

from lib.stream import GlobalStreamData


main_path = './client/'
child_path_data = main_path + 'data/'

class CreateNewNote(GlobalStreamData):
    def __init__(self, reader, writer, token):
        super(CreateNewNote, self).__init__(reader, writer)
        self.token = token

    async def new_note(self):
        while True:
            title = input('Title [.txt]: ')
            if input('Are you sute to create new note with title: ' + title + '? (y/n) ') == 'y':
                self.data = {'title': title + '.txt',
                             'text': '',
                             'token': self.token}
                self.action = 'new_note'
                await self.transfer_data()
                break
            else:
                continue


class GetAllNotes(GlobalStreamData):
    def __init__(self, reader, writer, token):
        super(GetAllNotes, self).__init__(reader, writer)
        self.token = token

    async def get_all(self):
        self.data = {'token': self.token}
        self.action = 'get_all_notes'
        await self.transfer_data()


class Note(GlobalStreamData):
    def __init__(self, reader, writer, token):
        super(Note, self).__init__(reader, writer)
        self.token = token

    async def print_action_with_note(self):
        print('[1]. Read\n'
              '[2]. Edit\n'
              '[3]. Delete\n'
              '[4]. Get all notes\n'
              '[5]. Back to menu\n')

    async def error_ops(self):
        print('Wrong action')
        await self.main()

    async def perform_ops_note(self, choose_ops):
        ops = {'1': self.read_note,
               '2': self.edit_note,
               '3': self.delete_note,
               '4': self.get_all_notes,
               '5': self.back}
        await ops.get(choose_ops, self.error_ops)()

    async def print_all_notes(self, data):
        print('\n\nPATH!\n')
        for i in range(1, len(data['path_user']) + 1):
            print(str(i) + '. ' + data['path_user'][i - 1])
        print('\n')

    async def get_all_notes(self):
        get = GetAllNotes(self.reader, self.writer, self.token)
        await get.get_all()
    
    async def print_note(self, data):
        print('\n')
        print('Title: ' + data['title'])
        print('Text:\n' + data['text'])
        print('\n')

    async def read_note(self):
        id_note = int(input('Choose note [number]: '))
        self.data = {
            'id_note': id_note,
            'token': self.token
        }
        self.action = 'read_note'
        await self.transfer_data()

    async def edit_note(self):
        id_note = int(input('Choose note [number]: '))
        self.data = {
            'id_note': id_note,
            'text': input('Text: '),
            'token': self.token
        }
        self.action = 'edit_note'
        await self.transfer_data()

    async def delete_note(self):
        id_note = int(input('Choose note [number]: '))
        self.data = {
            'id_note': id_note,
            'token': self.token
        }
        self.action = 'delete_note'
        await self.transfer_data()

    async def back(self):
        self.data = {
            'token': self.token
        }
        self.action = 'back_to_menu'
        await self.transfer_data()

    async def main(self):
        while True:
            await self.print_action_with_note()
            act = input('Choose action: ')
            await self.perform_ops_note(act)
            
            await self.read_data()

            if self.action == 'read_note':
                await self.print_note(self.data)
            elif self.action == 'get_all_notes':
                await self.print_all_notes(self.data)
            elif self.action == 'back_to_menu':
                break
            else:
                print(self.message)


class SyncNotes(GlobalStreamData):
    def __init__(self, reader, writer, token):
        super(SyncNotes, self).__init__(reader, writer)
        self.token = token

    async def print_sync_note(self):
        print('[1]. Sync with server\n'
              '[2]. Download with server\n'
              '[3]. Back to menu\n')

    async def error_ops(self):
        print('Wrong action')
        await self.main()

    async def perform_ops_note(self, choose_ops):
        ops = {'1': self.sync_notes,
               '2': self.download_notes,
               '3': self.main}
        await ops.get(choose_ops, self.error_ops)()
    
    async def upload_note(self, path):
        self.data = {
            'title': os.path.basename(path),
            'text': open(path, 'r').read(),
            'token': self.token
        }
        self.action = 'upload_note'
        await self.transfer_data()

    async def sync_notes(self):
        files = next(walk(child_path_data),
            (None, None, []))[2]
        list_files = list(map(lambda file: join(child_path_data, file), files))
        while True:
            for path in list_files:
                await self.upload_note(path)

            self.action = 'sync_notes_end'
            await self.transfer_data()
            break

    async def download_notes(self):
        self.data = {
            'token': self.token
        }
        self.action = 'download_notes'
        await self.transfer_data()
    
    async def save_to_local(self, data):
        with open(join(child_path_data, data['title']), 'w') as f:
            f.write(data['text'])
        self.data = {
            'title': data['title'],
        }
        self.action = 'save_to_local'
        await self.transfer_data()
    
    async def main(self):
        while True:
            await self.print_sync_note()
            act = input('Choose action: ')
            await self.perform_ops_note(act)

            while True:
                await self.read_data()
                if self.action == 'download_note':
                    await self.save_to_local(self.data)
                elif self.action == 'download_notes_end':
                    print(self.message)
                    break
