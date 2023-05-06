from fastapi import APIRouter, Depends, Path
from starlette import status

from src.auth.utils.auth_bearer import (
    UserPermission,
    get_permission
)
from src.lessons.crud import LessonCrud
from src.lessons.shemas import LessonBase, CommentBase

router = APIRouter(prefix='/lesson', tags=['Страница уроков курса'])


@router.get('/{course_id}', summary='Все уроки курса')
def get_all_lessons_current_course(
        course_id: int,
        lesson_crud: LessonCrud = Depends(),
):
    """Получить все уроки курса по его id."""
    return lesson_crud.get_all_course_lessons(course_id)


@router.get('/{course_id}/{lessons_id}')
def get_lesson_from_current_course(
        course_id: int,
        lessons_id: int,
        lesson_crud: LessonCrud = Depends(),
        permission: UserPermission = Depends(get_permission)
):
    """
    Возвращает урок по его id из курса. Если урок платный, или пользователь не получил доступ
    к курсу, то возвращает ответ 403.
    """
    return lesson_crud.get_lesson_from_course(
        course_id, lessons_id, permission)


@router.post('/{course_id}', status_code=status.HTTP_201_CREATED)
def add_lessons_to_course(
        course_id: int,
        lesson_data: LessonBase,
        lesson_crud: LessonCrud = Depends(),
        permission: UserPermission = Depends(get_permission)
):
    """
    Добавить курсу по его id новый урок.
    """
    return lesson_crud.add_lesson_to_course(course_id, lesson_data, permission)


@router.post('/pass/{lessons_id}')
def pass_lesson(
        lessons_id: int = Path(..., gt=0),
        lesson_crud: LessonCrud = Depends(),
        permission: UserPermission = Depends(get_permission)
):
    """
    Делает пометку в бд, что студент прошел данный урок и текущего курса.
    Обновляет время прохождения урока.
    """
    return lesson_crud.get_lesson_from_course(
        lessons_id, permission.user_email)


@router.post(
    '/{course_id}/{lesson_id}/add_comment',
    status_code=status.HTTP_201_CREATED,
    description='Добавить комментарий уроку по его id.',
    summary='Добавить комментарий'
)
def add_comment(
        comment_data: CommentBase,
        lesson_id: int = Path(..., gt=0),
        course_id: int = Path(..., gt=0),
        lesson_crud: LessonCrud = Depends(),
        permission: UserPermission = Depends(get_permission),

):
    lesson_crud.add_comment_to_lesson(
        comment_data, lesson_id, course_id, permission)
