import asyncio
import unittest
from typing import Final

from irc_client import IrcClient


async def handle_request(reader, writer):
    data = await reader.readline()
    print(data)


class IrcClientTests(unittest.IsolatedAsyncioTestCase):
    """Async irc client tests"""
    test_server_host: Final[str] = "127.1"
    test_server_port = 37337

    async def create_server(self):
        self._server = await asyncio.start_server(
            handle_request,
            "127.1",
            self.test_server_port,
            reuse_port=True,
            reuse_address=True
        )
        await self._server.start_serving()

    async def asyncSetUp(self):
        self._server_task = asyncio.create_task(self.create_server())
        await self._server_task

    async def asyncTearDown(self):
        self._server_task.cancel()

    async def test_irc_server_client_connection(self):
        """The client can connect to the server"""
        client = IrcClient()
        await client.connect(self.test_server_host, self.test_server_port)
        await client.disconnect()
        self.fail("Finish me!")

    async def test_bla(self):
        self.fail("Finish me!")
