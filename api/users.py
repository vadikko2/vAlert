from fastapi import APIRouter

router = APIRouter(
    prefix='/users'
)


@router.get('/{user}')
async def get_user(user: str):
    return user
