from fastapi import APIRouter, Depends, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from starlette.responses import JSONResponse

from vAlert.api.users.model import User
from vAlert.api.users.utils import get_current_user, get_current_active_user
from vAlert.config import VERSION

router = APIRouter(
    prefix='/'
)


@router.get('/openapi.json')
async def get_open_api_endpoint(request: Request, current_user: User = Depends(get_current_user)):
    return JSONResponse(get_openapi(title='vAlert', version=VERSION, routes=request.app.routes))


@router.get("/docs")
async def get_documentation(current_user: User = Depends(get_current_active_user)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
