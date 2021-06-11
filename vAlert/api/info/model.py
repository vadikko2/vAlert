from pydantic import BaseModel, Field


class CriticalType(BaseModel):
    id: int = Field(..., title='Идентификатор в базе даных')
    name: str = Field(..., title='Название типа критичности сообщения')