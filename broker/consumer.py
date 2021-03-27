import asyncio
from typing import Callable, Coroutine

import aio_pika
from get_messsage import *
from random import random

from constants import CRITICAL_TYPES, DEPARTURES, FREQUENCY_LIST
from utils import get_broker_connection

DISTRIBUTION = get_distribution([freq for _, freq in FREQUENCY_LIST])


async def basic_callback(message: aio_pika.IncomingMessage):
    print(message)


async def listen_one_from_queue(channel: aio_pika.Channel, queue_name: str):
    queue = await channel.get_queue(name=queue_name)
    return await queue.get(fail=None, no_ack=True)


async def collector(connection: aio_pika.Connection, callback: Callable[[aio_pika.IncomingMessage], Coroutine]):
    async with connection.channel() as channel:
        for queue_name in CRITICAL_TYPES:
            for exchange_name in DEPARTURES:
                queue = await channel.declare_queue(name=queue_name, durable=False, auto_delete=False)
                exchange = await channel.declare_exchange(name=exchange_name, durable=False, auto_delete=True)
                await queue.bind(exchange, queue.name)

        while True:
            penny = random()
            queue_name = FREQUENCY_LIST[get_index(penny, DISTRIBUTION)][0]
            message = await listen_one_from_queue(channel=channel, queue_name=queue_name)
            if not (message is None):
                await callback(message)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    broker_c = loop.run_until_complete(get_broker_connection(loop))  # type: aio_pika.Connection

    try:
        loop.run_until_complete(collector(connection=broker_c, callback=basic_callback))
    finally:
        loop.run_until_complete(broker_c.close())
