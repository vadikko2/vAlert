from random import random
from typing import Callable, Coroutine

from aio_pika import Connection, Channel

from broker.consumer import listen_one_from_queue
from broker.get_messsage import get_distribution, get_index
from constants import FREQUENCY_LIST, COLLECTOR_EXCHANGE_NAME, COLLECTOR_QUEUE_NAME

DISTRIBUTION = get_distribution([freq for _, freq in FREQUENCY_LIST])


async def collector(connection: Connection, callback: Callable[[bytes, str, str, Channel], Coroutine]):
    async with connection.channel() as channel:
        while True:
            penny = random()
            queue_name = FREQUENCY_LIST[get_index(penny, DISTRIBUTION)][0]
            message = await listen_one_from_queue(channel=channel, queue_name=queue_name)
            if not (message is None):
                await callback(message.body, COLLECTOR_EXCHANGE_NAME, COLLECTOR_QUEUE_NAME, channel)
