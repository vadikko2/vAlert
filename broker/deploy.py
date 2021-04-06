from aio_pika import Connection

from constants import (
    CRITICAL_TYPES, DEPARTURES,
    COLLECTOR_QUEUE_NAME, COLLECTOR_EXCHANGE_NAME
)


async def deploy_infra(connection: Connection):
    async with connection.channel() as channel:
        for queue_name in CRITICAL_TYPES:
            for exchange_name in DEPARTURES:
                queue = await channel.declare_queue(name=queue_name, durable=False, auto_delete=False)
                exchange = await channel.declare_exchange(name=exchange_name, durable=False, auto_delete=True)
                await queue.bind(exchange, queue.name)

        queue = await channel.declare_queue(name=COLLECTOR_QUEUE_NAME, durable=False, auto_delete=False)
        exchange = await channel.declare_exchange(name=COLLECTOR_EXCHANGE_NAME, durable=False, auto_delete=True)
        await queue.bind(exchange, queue.name)
