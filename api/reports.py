from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Request, Cookie, Response

from api.models import ReportCreated, Report, Resolver
from broker.publisher import publish

router = APIRouter(
    prefix='/reports'
)


@router.post('/create', response_model=ReportCreated)
async def create_report(report: Report, request: Request, response: Response):
    uuid = report.id
    departure = report.departure
    critical = report.critical
    await publish(request.app.extra['broker_connection'], str(uuid), departure, critical)
    response.set_cookie(key='user_uuid', value=str(uuid))  # todo это просот пример того, как в FastAPI работает cookie
    return ReportCreated(created_datetime=report.date, uuid=uuid)


@router.get('/get', response_model=UUID)
async def get_report(user_uuid: Optional[UUID] = Cookie(None)):
    # todo обращаемся к раббиту и по полученной заявке обновляем в БД поле resolver
    if not user_uuid:
        return None
    else:
        return user_uuid
