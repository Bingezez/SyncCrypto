import asyncio

from lib import network
from server_interface import Interface
from lib.utils import deserialize, create_folder
from lib.database.client_db import RegisterNewClient

name_db = 'client.db'
main_path = './server/'
child_path_db = main_path + 'database/'
child_path_key = main_path + 'key/'
child_path_data = main_path + 'data/'
child_path_session = main_path + 'session/'


class Server(network.Server):
    def __init__(self, host, port):
        super(Server, self).__init__(host, port)
        self.loop = None
        self._db = None

    async def main_init(self):
        self._db = RegisterNewClient(name_db, child_path_db)
        self._db.create_tbl()
        await create_folder(child_path_key)
        await create_folder(child_path_data)
        await create_folder(child_path_session)

    async def handle_client(self, reader, writer):
        await asyncio.gather(self.main_init())
        interface = Interface(reader, writer, self._db)
        await interface.main()

    def __enter__(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.server_start())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.loop.run_until_complete(self.close())

    def __str__(self):
        return 'Start server: {}:{}'.format(self.host, self.port)

    def __del__(self):
        self.loop.close()


if __name__ == '__main__':
    with open('config/config_server.json', 'r') as f:
        conf = deserialize(f.read())
    try:
        with Server(conf['host'], conf['port']) as server:
            pass
    except KeyboardInterrupt:
        print('Server stopped')
        pass