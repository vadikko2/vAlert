import asyncio

import aio_pika
from fastapi import FastAPI

from api.models import Report, ReportCreated
from broker.publisher import publish
from broker.utils import get_broker_connection

app = FastAPI()


@app.on_event('startup')
async def connect_to_broker():
    loop = asyncio.get_event_loop()
    app.extra['broker_connection'] = await get_broker_connection(loop)  # type: aio_pika.Connection


@app.on_event('shutdown')
async def close_broker_connection():
    await app.extra['broker_connection'].close()


@app.post('/report', response_model=ReportCreated)
async def create_report(report: Report):
    uuid = report.id
    departure = report.departure
    critical = report.critical

    await publish(app.extra['broker_connection'], str(uuid), departure, critical)
    return ReportCreated(created_datetime=report.date, uuid=uuid)
