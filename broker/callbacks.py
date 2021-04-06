from aio_pika import IncomingMessage, Channel, Message


async def basic_callback(message: IncomingMessage):
    print(message)


async def collector_callback(message: bytes, exchange_name: str, routing_key: str, channel: Channel):
    exchange = await channel.declare_exchange(name=exchange_name, durable=False, auto_delete=True)
    await exchange.publish(message=Message(body=message), routing_key=routing_key)
