import aio_pika


async def get_broker_connection(loop) -> aio_pika.Connection:
    connection = await aio_pika.connect(
        host='localhost',
        login='guest',
        password='guest',
        loop=loop
    )  # type: aio_pika.Connection
    return connection
