import asyncio

from lib import network
from client_interface import Interface
from lib.utils import deserialize, create_folder


main_path = './client/'
child_path_key = main_path + 'key/'
child_path_data = main_path + 'data/'
child_path_session = main_path + 'session/'


class Client(network.Client):
    def __init__(self, host, port):
        super(Client, self).__init__(host, port)
        self.loop = None

    async def main_init(self):
        await create_folder(child_path_key)
        await create_folder(child_path_data)
        await create_folder(child_path_session)

    async def session(self):
        await asyncio.gather(self.main_init())
        interface = Interface(self.reader, self.writer)
        await interface.main()
        print('hello')


    def __enter__(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.connect())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.loop.run_until_complete(self.close())

    def __del__(self):
        self.loop.close()


if __name__ == '__main__':
    with open('config/config_client.json', 'r') as f:
        conf = deserialize(f.read())
    try:
        with Client(conf['server'], conf['port']) as client:
            print('Connected to server')
            client.loop.run_until_complete(client.session())
            print('Disconnected from server')
    except KeyboardInterrupt:
        pass
