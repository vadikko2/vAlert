from pydantic import BaseModel, Field


class Token(BaseModel):
    token: str = Field(..., title='Токен')
    type: str = Field(..., title='Тип')


class TokenData(BaseModel):
    username: str = Field(..., title='Имя пользователя')
