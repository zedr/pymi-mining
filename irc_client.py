#!/usr/bin/env python3
import asyncio


class IrcClient:
    async def connect(
        self, server_host: str = "127.1", server_port: int = 6667
    ) -> None:
        """Connect to an IRC server"""
        self.reader, self.writer = await asyncio.open_connection(
            server_host, server_port
        )

    async def disconnect(self) -> None:
        """Disconnect from the IRC server"""
        self.writer.close()
        await self.writer.wait_closed()

    async def send(self, message: str) -> None:
        """Send a message to the server"""
        self.writer.write(message.encode() + b"\r\n")
        await self.writer.drain()


if __name__ == "__main__":
    try:
        pass
    except KeyboardInterrupt:
        pass
