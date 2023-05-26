"""
Здесь находятся endpoints для отображения и работы с опросами после прохождения урок.
"""
from fastapi import APIRouter, Depends

from src.poll.crud import PollCrud

router = APIRouter(prefix='/poll', tags=['Опрос'])


@router.get('/', )
def get_main(poll_crud: PollCrud = Depends()):
    return poll_crud.get_all_polls()
