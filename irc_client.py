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

    async def set_nick(self, nick_name: str) -> None:
        """Set the nick of the client"""
        await self.send(f"NICK {nick_name}")

    async def set_user(self, user_name: str) -> None:
        """Set the user identity of the client"""
        await self.send(f"USER {user_name} 0 * :{user_name}")

    async def join_channel(self, channel_name: str) -> None:
        """Join a channel"""
        await self.send(f"JOIN #{channel_name}")

    async def send_message(self, channel_name: str, message: str) -> None:
        """Send a message to the given channel"""
        await self.send(f"PRIVMSG #{channel_name} :{message}")


if __name__ == "__main__":
    try:
        pass
    except KeyboardInterrupt:
        pass
