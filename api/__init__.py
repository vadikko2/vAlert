import asyncio
from aio_pika import Connection
from fastapi import FastAPI

from broker.utils import get_broker_connection
from api import reports
from api import users

app = FastAPI()


@app.on_event('startup')
async def connect_to_broker():
    loop = asyncio.get_event_loop()
    app.extra['broker_connection'] = await get_broker_connection(loop)  # type: Connection


@app.on_event('shutdown')
async def close_broker_connection():
    await app.extra['broker_connection'].close()


app.include_router(reports.router)
app.include_router(users.router)
