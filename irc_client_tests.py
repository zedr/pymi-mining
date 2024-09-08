import unittest

from irc_client import IrcClient


class IrcClientTests(unittest.IsolatedAsyncioTestCase):
    """Async irc client tests"""

    async def test_irc_server_client_connection(self):
        """The client can connect to the server"""
        client = IrcClient()
        self.fail("Finish me!")
