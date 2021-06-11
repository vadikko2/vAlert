from fastapi import APIRouter
from typing import List

from vAlert.api.info.model import CriticalType

router = APIRouter(
    prefix='/info'
)


@router.get('/critical-types', response_model=List[CriticalType])
def critical_type():
    return [CriticalType(id=i, name=str(i)) for i in range(10)]
