import secrets
from typing import Optional
from uuid import UUID
from hashlib import md5

from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from vAlert.api.users.models import UserInDB

security = HTTPBasic()

fake_users_db = {
    "user1": {
        "user_uuid": UUID(md5(b"123456789").hexdigest()),
        "username": "user1",
        "full_name": "USER NUMBER ONE",
        "email": "user1@example.com",
        "hashed_password": md5(b"123").hexdigest(),
        "disabled": False,
    },
    "user2": {
        "user_uuid": UUID(md5(b"987654321").hexdigest()),
        "username": "user2",
        "full_name": "USER NUMBER TWO",
        "email": "user2@example.com",
        "hashed_password": md5(b"321").hexdigest(),
        "disabled": True,
    },
}


def get_user(db, username: str):  # todo db здесь должна быть сессия с БД
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed login",
            headers={"WWW-Authenticate": "Basic"},
        )


def auth(credentials: HTTPBasicCredentials = Depends(security)):
    # todo тут надо слазить в базу и взять оттуда md5
    # todo от полученного пароля надо взять md5 и сравить его с md5 из базы
    user = get_user(fake_users_db, credentials.username)
    correct_username = secrets.compare_digest(credentials.username, user.username)
    correct_password = secrets.compare_digest(md5(credentials.password.encode('utf-8')).hexdigest(),
                                              user.hashed_password)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user.user_uuid


def secure_mode(user_uuid: Optional[UUID] = Cookie(None), auth_user_uuid=Depends(auth)):
    if not auth_user_uuid == user_uuid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="UUID from cookie and UUID from auth is not the same.",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user_uuid
