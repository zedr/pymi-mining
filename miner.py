#!/usr/bin/env python3
import asyncio
import random

from irc_client import IrcClient
from mining_hash import mine


class Miner(IrcClient):
    """
    A broadcasting client that issues mining requests and processes responses
    """

    channel: str = "pymi"
    difficulty: int = 5

    def __init__(self):
        self.begin_nonce: int = random.randint(1, 1000)
        self._busy = False

    async def process_mining_request(self, src, cmd, msgs) -> None:
        """Process a mining request"""
        if self._busy:
            return
        try:
            _, request, *words = msgs
        except ValueError:
            pass
        else:
            if request == ":REQUEST":
                msg = " ".join(words)
                await self.send_message(self.channel, "Mining...")
                self._busy = True
                result = mine(msg, self.difficulty, self.begin_nonce)
                await self.send_message(self.channel, f"MINED {result}")
                self._busy = False

    async def run(self):
        await self.connect()
        await self.set_nick(f"miner49er-{self.begin_nonce}")
        await self.set_user(f"miner49er-{self.begin_nonce}")
        await self.join_channel(self.channel)
        await self.send_message("pymi", "Hello there")
        try:
            await self.handle_forever(handlers=(self.echo, self.process_mining_request))
        finally:
            await self.disconnect()


async def main():
    client = Miner()
    await client.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
