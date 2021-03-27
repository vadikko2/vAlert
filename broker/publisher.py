import aio_pika

from constants import CRITICAL_TYPES, DEPARTURES


async def publish(connection: aio_pika.Connection, message: str, departure: str, critical_type: str):
    async with connection.channel() as channel:

        departure = departure.lower().strip()
        if departure in DEPARTURES:
            exchange = await channel.declare_exchange(name=departure, durable=False, auto_delete=True)
        else:
            raise Exception(f'Нет такого отдела')

        if not (critical_type in CRITICAL_TYPES):
            raise Exception('Неизветный тип критичности')

        await exchange.publish(message=aio_pika.Message(message.encode('utf-8')), routing_key=critical_type)
