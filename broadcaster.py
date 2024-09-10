import asyncio
import random
import datetime as dt
from typing import Optional

from irc_client import IrcClient
from mining_hash import verify, md5hash

NAMES = (
    "Bob",
    "Alice",
    "Eve",
)


class Broadcaster(IrcClient):
    """
    A broadcasting client that issues mining requests and processes responses
    """

    channel: str = "pymi"
    difficulty: int = 5

    def __init__(self):
        self.last_request: Optional[str] = None
        self.last_request_dt = dt.datetime.now()

    async def repeat_mining_request(self, src, cmd, _) -> None:
        """Repeat the mining request when a user joins"""
        if cmd == "JOIN":
            if msg := self.last_request:
                await self.send_message(self.channel, "REQUEST " + msg)

    async def send_mining_request(self) -> None:
        """Send a mining request to the channel"""
        peer1 = random.choice(NAMES)
        peer2 = random.choice(NAMES)
        amount = random.randint(1, 100)
        self.last_request = msg = f"{peer1} sent {amount} to {peer2}"
        self.last_request_dt = dt.datetime.now()
        await self.send_message(self.channel, "REQUEST " + msg)

    async def verify_miner_response(self, src, cmd, msgs) -> None:
        """Verify a response given by a miner"""
        try:
            _, response, nonce = msgs
        except ValueError:
            pass
        else:
            if response == ":MINED":
                to_hash = f"{nonce}{self.last_request}"
                hashed = md5hash(to_hash)
                if verify(hashed, self.difficulty):
                    delta_dt = dt.datetime.now() - self.last_request_dt
                    await self.send_message(
                        self.channel,
                        (
                            f"{src} mined block "
                            f"in {delta_dt.seconds} secs: "
                            f"{hashed}: "
                            f"{self.last_request}"
                        ),
                    )
                    await self.send_mining_request()
                else:
                    await self.send_message(self.channel, "LIAR!!!")

    async def run(self):
        await self.connect()
        await self.set_nick("rigelbot")
        await self.set_user("rigelbot")
        await self.join_channel(self.channel)
        await self.send_message("pymi", "Hello there")
        await self.send_mining_request()
        try:
            await self.handle_forever(
                handlers=(
                    self.echo,
                    self.verify_miner_response,
                    self.repeat_mining_request,
                )
            )
        finally:
            await self.disconnect()


async def main():
    client = Broadcaster()
    await client.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
