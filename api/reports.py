from typing import Optional
from uuid import UUID

from aio_pika import Connection, IncomingMessage
from fastapi import APIRouter, Request, Cookie, HTTPException

from constants import COLLECTOR_QUEUE_NAME
from api.models import ReportCreated, Report, ReportAssigned
from broker.publisher import publish_report
from broker.consumer import listen_one_from_queue

router = APIRouter(
    prefix='/reports'
)


@router.post('/create', response_model=ReportCreated)
async def create_report(report: Report, request: Request):
    uuid = report.id
    departure = report.departure
    critical = report.critical
    await publish_report(request.app.extra['broker_connection'], str(uuid), departure, critical)
    return ReportCreated(created_datetime=report.date, uuid=uuid)


@router.get('/get', response_model=ReportAssigned)  # todo должен возвращать Report
async def get_report(request: Request, user_uuid: Optional[UUID] = Cookie(None)):
    if not user_uuid:
        return False
    else:
        connection = request.app.extra['broker_connection']  # type: Connection
        async with connection.channel() as channel:
            message = await listen_one_from_queue(
                channel=channel,
                queue_name=COLLECTOR_QUEUE_NAME
            )  # type: Optional[IncomingMessage]

            if message is None:
                raise HTTPException(status_code=404, detail="Нет заявок доступных для выполнения")
            else:
                response = ReportAssigned(id=message.body.decode('utf-8'))

            # todo тут должен быть в БД по UUID и должен формироваться объект Report
            # todo тут должен быть запрос в БД, который проставляет resolver для заявки

            return response
