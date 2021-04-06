import asyncio
from typing import Callable, Coroutine
from aio_pika import Connection, IncomingMessage, Channel
from get_messsage import *
from random import random

from constants import FREQUENCY_LIST
from utils import get_broker_connection

DISTRIBUTION = get_distribution([freq for _, freq in FREQUENCY_LIST])


async def basic_callback(message: IncomingMessage):
    print(message)


async def listen_one_from_queue(channel: Channel, queue_name: str):
    queue = await channel.declare_queue(name=queue_name, durable=False, auto_delete=False)
    return await queue.get(fail=None, no_ack=True)


async def collector(connection: Connection, callback: Callable[[IncomingMessage], Coroutine]):
    async with connection.channel() as channel:
        while True:
            penny = random()
            queue_name = FREQUENCY_LIST[get_index(penny, DISTRIBUTION)][0]
            message = await listen_one_from_queue(channel=channel, queue_name=queue_name)
            if not (message is None):
                await callback(message)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    broker_c = loop.run_until_complete(get_broker_connection(loop))  # type: Connection

    try:
        loop.run_until_complete(collector(connection=broker_c, callback=basic_callback))
    finally:
        loop.run_until_complete(broker_c.close())
