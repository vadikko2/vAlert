from uuid import uuid4, UUID

from fastapi import APIRouter, Response

router = APIRouter(
    prefix='/users'
)


@router.get('/{user}')
async def get_user(user: str):
    return user


@router.get('/login', response_model=UUID)
async def login(response: Response):
    # todo супер тупая заглука аутентификации тупо для того, что бы ну хоть что-то было в куки
    uuid = uuid4()
    response.set_cookie(key='user_uuid', value=str(uuid))
    return uuid
