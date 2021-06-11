from fastapi import APIRouter, Response, Depends

router = APIRouter(
    prefix='/users'
)


# @router.get('/user/{user}')
# async def get_user(user: str):
#     return user
#
#
# @router.get('/login', response_model=Login)
# async def login(response: Response, user_uuid=Depends(auth)):
#     response.set_cookie(key='user_uuid', value=str(user_uuid))
#     return Login(user_uuid=user_uuid)
