from typing import Optional

from pydantic import Field
from pydantic.main import BaseModel


class Role(BaseModel):
    id: int = Field(..., title='Идентификатор роли')
    name: str = Field(..., title='Наименование роли')


class Subdivision(BaseModel):
    id: int = Field(..., title='Идентификатор подразделения')
    name: str = Field(..., title='Наименование подраздедения')
    parent_subdivision: int = Field(..., title='Идентификатор родителя')


class Position(BaseModel):
    id: int = Field(..., title='Идентификатор позиции в базе')
    name: str = Field(..., title='Наименование позиции')
    subdivision: Subdivision = Field(..., title='Подразделение')
    parent_position: int = Field(..., title='Идентификатор родителя')


class User(BaseModel):
    id: int = Field(..., title='Идентификатор пользователя в базе данных')
    first_name: str = Field(..., title='Имя')
    last_name: str = Field(..., title='Фамилия')
    patronymic: str = Field(..., title='Отчество')
    email: Optional[str] = Field(..., title='Адрес электронной почты')
    phone: Optional[str] = Field(..., title='Номер телефона')
    disabled: Optional[bool] = Field(default=False, title='Активный пользователь')
    position: Position = Field(..., title='Должность')
    role: Role = Field(..., title='Роль')


class UserInDB(User):
    password_hash: str = Field(..., title='Хэш от пароля')
