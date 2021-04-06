from aio_pika import Channel, IncomingMessage


async def listen_one_from_queue(channel: Channel, queue_name: str) -> IncomingMessage:
    queue = await channel.declare_queue(name=queue_name, durable=False, auto_delete=False)
    return await queue.get(fail=None, no_ack=True)
