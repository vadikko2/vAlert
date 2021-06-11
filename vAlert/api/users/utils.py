from datetime import timedelta, datetime
from hashlib import md5
from uuid import UUID
from jwt import PyJWTError
import jwt

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic
from starlette.status import HTTP_403_FORBIDDEN

from vAlert.api.auth.model import TokenData
from vAlert.api.auth.utils import oauth2_scheme, verify_password
from vAlert.api.users.model import UserInDB, User
from vAlert.config import settings

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


def get_user(db, username: str) -> UserInDB:
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


async def get_current_user(token: str = Depends(oauth2_scheme), jwt=None):
    credentials_exception = HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except PyJWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
