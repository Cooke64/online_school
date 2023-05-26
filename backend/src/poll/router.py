"""
Здесь находятся endpoints для отображения и работы с опросами после прохождения урок.
Так же здесь находятся endpoints для работы с вопросами к опросу.
"""
from fastapi import APIRouter, Depends

from src.auth.utils.auth_bearer import UserPermission, get_permission
from src.poll.crud import PollCrud
from src.poll.schemas import PollBase

router = APIRouter(prefix='/poll', tags=['Опрос'])


@router.get('/', )
def get_main(poll_crud: PollCrud = Depends()):
    return poll_crud.get_all_polls()


@router.post('/create_poll/{course_id}/{lesson_id}',
             summary='Создать новый опрос к уроку', )
def create_poll(
        lesson_id: int,
        poll_data: PollBase,
        permission: UserPermission = Depends(get_permission),
        poll_crud: PollCrud = Depends()):
    return poll_crud.add_poll_to_lesson(lesson_id, poll_data, permission)


@router.delete('/remove_poll/{course_id}/{lesson_id}',
               summary='Удалить опрос', )
def remove_poll(
        lesson_id: int,
        permission: UserPermission = Depends(get_permission),
        poll_crud: PollCrud = Depends()):
    return poll_crud.remove_poll(lesson_id, permission)
