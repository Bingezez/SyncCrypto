from os.path import join

from lib.stream import GlobalStreamData

session_file = 'my_session.txt'
path_session = './client/session/'


class Token(GlobalStreamData):
    def __init__(self, reader, writer):
        super(Token, self).__init__(reader, writer)

    async def save_token(self, data):
        with open(join(path_session, session_file), 'w') as f:
            f.write(data['token'])

    async def read_token(self):
        with open(join(path_session, session_file), 'r') as f:
            return f.read()