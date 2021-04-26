import aio_pika
from vAlert.config import settings


async def get_broker_connection(loop) -> aio_pika.Connection:
    connection = await aio_pika.connect(
        host=settings.RABBIT.host,
        login=settings.RABBIT.user,
        password=settings.RABBIT.password,
        port=settings.RABBIT.port,
        loop=loop
    )  # type: aio_pika.Connection
    return connection
