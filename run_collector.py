import asyncio

from aio_pika import Connection

from broker.callbacks import collector_callback
from broker.utils import get_broker_connection
from collector.daemon import collector

if __name__ == '__main__':
    """
    Поднимает демона c коллектором, который будует постоянно слушать очереди с приоритетами
    и складывать заявки в одну очередь (reports)
    """
    loop = asyncio.get_event_loop()

    broker_c = loop.run_until_complete(get_broker_connection(loop))  # type: Connection

    try:
        loop.run_until_complete(collector(connection=broker_c, callback=collector_callback))
    finally:
        loop.run_until_complete(broker_c.close())
