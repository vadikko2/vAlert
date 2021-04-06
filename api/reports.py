from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Request, Cookie

from api.models import ReportCreated, Report
from broker.publisher import publish

router = APIRouter(
    prefix='/reports'
)


@router.post('/create', response_model=ReportCreated)
async def create_report(report: Report, request: Request):
    uuid = report.id
    departure = report.departure
    critical = report.critical
    await publish(request.app.extra['broker_connection'], str(uuid), departure, critical)
    return ReportCreated(created_datetime=report.date, uuid=uuid)


@router.get('/get', response_model=bool)  # todo должен возвращать Report
async def get_report(user_uuid: Optional[UUID] = Cookie(None)):
    # todo обращаемся к раббиту и по полученной заявке обновляем в БД поле resolver
    if not user_uuid:
        return False
    else:
        return True  # todo тут надо вернуть ральный Report, полученный из базы по uuid из раббита
