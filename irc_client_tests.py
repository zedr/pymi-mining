import asyncio
import unittest
from typing import Final

from irc_client import IrcClient


class FakeIrcServer:
    def __init__(self):
        self.messages = []
        self.received = asyncio.Event()

    async def handle_request(self, reader, writer):
        data = await reader.readline()
        self.messages.append(data)
        self.received.set()


class IrcClientTests(unittest.IsolatedAsyncioTestCase):
    """Async irc client tests"""

    test_server_host: Final[str] = "127.1"
    test_server_port = 37337

    async def create_server(self):
        self._irc_server = FakeIrcServer()
        self._server = await asyncio.start_server(
            self._irc_server.handle_request,
            "127.1",
            self.test_server_port,
            reuse_port=True,
            reuse_address=True,
        )
        await self._server.start_serving()

    async def asyncSetUp(self):
        self._server_task = asyncio.create_task(self.create_server())
        await self._server_task

    async def asyncTearDown(self):
        self._server_task.cancel()
        self._server.close()

    async def test_client_connection(self):
        """The client can connect to the server"""
        client = IrcClient()
        await client.connect(self.test_server_host, self.test_server_port)
        await client.disconnect()

    async def test_client_sending_message(self):
        client = IrcClient()
        await client.connect(self.test_server_host, self.test_server_port)
        await client.send("PING")
        await self._irc_server.received.wait()
        self.assertEqual([b"PING\r\n"], self._irc_server.messages)
        await client.disconnect()

    async def test_client_set_nick(self):
        client = IrcClient()
        await client.connect(self.test_server_host, self.test_server_port)
        await client.set_nick("zedr")
        await self._irc_server.received.wait()
        self.assertEqual([b"NICK zedr\r\n"], self._irc_server.messages)
        await client.disconnect()


if __name__ == "__main__":
    unittest.main()
