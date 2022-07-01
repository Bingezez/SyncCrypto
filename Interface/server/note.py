import os
import datetime

from os import walk
from os.path import join
from lib.stream import GlobalStreamData

data_path = './server/data'


class CreateNewNote(GlobalStreamData):
    def __init__(self, reader, writer):
        super(CreateNewNote, self).__init__(reader, writer)

    async def new_note(self, data, path_user):
        self.action = 'new_note'
        path = join(data_path, path_user, data['title'])
        if os.path.isfile(path):
            self.status = 'error'
            self.message = 'File already exist!'
        else:
            self.status = 'success'
            self.message = 'File created!'
            with open(path, 'w') as f:
                f.write(data['text'])
        await self.transfer_data()


class PathUser(GlobalStreamData):
    def __init__(self, reader, writer):
        super(PathUser, self).__init__(reader, writer)

    async def send(self, path_user):
        self.data = {
            'path_user': next(walk(join(data_path, path_user)),
                              (None, None, []))[2]
        }
        self.action = 'get_all_notes'
        await self.transfer_data()


class Note(GlobalStreamData):
    def __init__(self, reader, writer):
        super(Note, self).__init__(reader, writer)

    async def read_note(self, data, path_user):
        self.action = 'read_note'
        file = next(walk(join(data_path, path_user)),
                    (None, None, []))[2]
        path = join(data_path,
                    path_user,
                    file[int(data['id_note']) - 1])
        if os.path.isfile(path):
            self.status = 'success'
            f = open(path, 'r')
            self.data = {
                'text': f.read(),
                'title': file[int(data['id_note']) - 1]
            }
            f.close()
        else:
            self.status = 'error'
            self.message = 'File not found!'
        await self.transfer_data()

    async def edit_note(self, data, path_user):
        self.action = 'edit_note'
        file = next(walk(join(data_path, path_user)),
                    (None, None, []))[2]
        path = join(data_path,
                    path_user,
                    file[int(data['id_note']) - 1])
        if os.path.isfile(path):
            self.status = 'success'
            f = open(path, 'a')
            f.write(f'{datetime.time()}\n')
            f.write(data['text'] + '\n')
            f.close()
        else:
            self.status = 'error'
            self.message = 'File not found!'
        await self.transfer_data()
    
    async def delete_note(self, data, path_user):
        self.action = 'delete_note'
        file = next(walk(join(data_path, path_user)),
                    (None, None, []))[2]
        path = join(data_path,
                    path_user,
                    file[int(data['id_note']) - 1])
        if os.path.isfile(path):
            self.status = 'success'
            os.remove(path)
        else:
            self.status = 'error'
            self.message = 'File not found!'
        await self.transfer_data()

class SyncNotes(GlobalStreamData):
    def __init__(self, reader, writer):
        super(SyncNotes, self).__init__(reader, writer)
    
    async def upload_note(self, data, path_user):
        # print(data['title'])
        # print(join(path_user, data['title']))
        path = data_path+'/'+path_user+'/'+data['title']

        print(path)
        if os.path.isfile(path):
            f = open(path, 'r')
            print(f)
            text = f.read()
            f.close()
            f = open(path, 'w')
            f.write(text + data['text'])
            print(f.read())
            f.close()

    async def sync_notes(self, data, path_user):
        while True:
            await self.upload_note(data, path_user)
            await self.read_data()
            if self.action == 'sync_notes_end':
                break


    async def download_note(self, path):       
        self.data = {
            'title': os.path.basename(path),
            'text': open(path, 'r').read()
        }
        self.action = 'download_note'
        await self.transfer_data()
    
    async def download_notes(self, path_user):
        print(1)
        files = next(walk(join(data_path, path_user)),
            (None, None, []))[2]
        list_files = list(map(lambda file: join(data_path, path_user, file), files))
        while True:
            for path in list_files:
                print(path)
                await self.download_note(path)
                await self.read_data()
        
            self.action = 'download_notes_end'
            self.message = 'Download end!'
            await self.transfer_data()
            break
        