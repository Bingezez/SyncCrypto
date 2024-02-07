from lib.utils import *


class _StreamData:
    def __init__(self, reader, writer):
        self._size = 4096
        self.reader = reader
        self.writer = writer

    async def _read(self):
        return await self.reader.read(self._size)

    async def _write(self, data):
        self.writer.write(data)
        await self.writer.drain()

    async def read(self):
        return decode(await self._read())

    async def write(self, data):
        await self._write(encode(data))

    async def read_json(self):
        return deserialize(await self.read())

    async def write_json(self, data):
        await self.write(serialize(data))

    async def close(self):
        self.writer.close()


class _Transfer(_StreamData):
    def __init__(self, reader, writer):
        super(_Transfer, self).__init__(reader, writer)
        self.data = None
        self.action = None
        self.status = None
        self.message = None

    async def transfer_data(self):
        await self.write_json({
            'data': self.data,
            'action': self.action,
            'status': self.status,
            'message': self.message
        })
        print({
            'data': self.data,
            'action': self.action,
            'status': self.status,
            'message': self.message
        })



class _Reader(_StreamData):
    def __init__(self, reader, writer):
        super(_Reader, self).__init__(reader, writer)
        self.data = None
        self.action = None
        self.status = None
        self.message = None

    async def read_data(self):
        data = await self.read_json()
        self.data = data['data']
        self.action = data['action']
        self.status = data['status']
        self.message = data['message']


class GlobalStreamData(_Transfer, _Reader, _StreamData):
    def __init__(self, reader, writer):
        super(GlobalStreamData, self).__init__(reader, writer)
