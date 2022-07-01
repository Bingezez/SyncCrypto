import asyncio


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = None

    async def server_start(self):
        self.server = await asyncio.start_server(
            self.handle_client,
            self.host,
            self.port
        )
        async with self.server:
            await self.server.serve_forever()

    async def handle_client(self, reader, writer):
        """main loop for handling client"""
        pass

    async def close(self):
        self.server.close()
        await self.server.wait_closed()


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(
            self.host,
            self.port
        )

    async def close(self):
        self.writer.close()
        await self.writer.wait_closed()
