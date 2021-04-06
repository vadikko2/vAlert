import asyncio
from aio_pika import Connection
from fastapi import FastAPI

from broker.utils import get_broker_connection
from broker.deploy import deploy_infra
from api import reports, users

app = FastAPI()


@app.on_event('startup')
async def connect_to_broker():
    loop = asyncio.get_event_loop()
    app.extra['broker_connection'] = await get_broker_connection(loop)  # type: Connection


@app.on_event('startup')
async def deploy_broker_infra():
    """
    Разворачивает инфраструктуру внутри раббита (создает все необходимые exchanges/queues/binds).
    Информацию для развертывания берет в constants.py (названия департаментов и приоритеты)
    """
    await deploy_infra(app.extra['broker_connection'])


@app.on_event('startup')
async def run_collector_daemon():
    """
    Поднимает демона c коллектором, который будует постоянно слушать очереди с приоритетами
    и складывать заявки в одну очередь (reports)
    """
    pass


@app.on_event('shutdown')
async def close_broker_connection():
    await app.extra['broker_connection'].close()


app.include_router(reports.router)
app.include_router(users.router)
