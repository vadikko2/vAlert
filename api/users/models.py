from typing import Optional
from uuid import UUID

from pydantic.main import BaseModel


class Login(BaseModel):
    user_uuid: UUID


class User(BaseModel):
    user_uuid: UUID
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str
