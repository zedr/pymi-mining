import asyncio


class IrcClient:

    async def connect(
            self,
            server_host: str = "127.1",
            server_port: int = 6667
    ):
        """Connect to an IRC server"""
        self.reader, self.writer = await asyncio.open_connection(
            server_host,
            server_port
        )

    async def disconnect(self):
        """Disconnect from the IRC server"""
        self.writer.close()
        await self.writer.wait_closed()


async def main():
    client = IrcClient()
    await client.connect()
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
