from pydantic import BaseModel, validator, Field

from datetime import datetime
from uuid import UUID, uuid4

from constants import DEPARTURES, CRITICAL_TYPES


class ReportCreated(BaseModel):
    uuid: UUID
    created_datetime: datetime


class Reporter(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    position: str = None
    address: str
    email: str


class Resolver(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    position: str = None
    address: str
    email: str


class Report(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    description: str
    date: datetime = Field(default_factory=datetime.now)
    reporter: Reporter
    departure: str
    critical: str
    resolver: Resolver = None

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
