from pydantic import BaseModel, validator, Field

from datetime import datetime
from uuid import UUID

from constants import DEPARTURES, CRITICAL_TYPES
from vAlert.api.info.model import CriticalType
from vAlert.api.users.model import User


class Report(BaseModel):
    id: int = Field(..., title='Идентификатор заявки в базе данных')
    title: str = Field(..., title='Название заявки')
    description: str = Field(..., title='Описание проблемы')
    timestamp: datetime = Field(default_factory=datetime.now, title='Веременная метка (default=datetime.now)')
    reporter: User = Field(..., title='Идентификатор создателя заявки')
    departure: str = Field(..., title='Отдел, в рамках которого возникла проблема.')
    critical: CriticalType = Field(..., title='Степень критичности')
    resolver: User = Field(..., )

    @validator('departure')
    def validate_departure_name(cls, v):
        if not (v in DEPARTURES):
            raise ValueError('Неизветный отдел')
        return v

    @validator('critical')
    def validate_critical_type(cls, v):
        if not (v in CRITICAL_TYPES):
            raise ValueError('Неизвестная степень критичности')
        return v


class ReportAssigned(BaseModel):
    id: UUID
    # report: Report # todo раскоментировать когда будем получать заявки из базы
    date: datetime = Field(default_factory=datetime.now)
    resolver_uuid: UUID


class ReportCreated(BaseModel):
    uuid: UUID
    created_datetime: datetime
    creator_uuid: UUID
