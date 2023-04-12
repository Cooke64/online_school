from fastapi import APIRouter, Depends

from src.auth.utils.auth_bearer import (
    UserPermission,
    get_permission,
    JWTBearer
)
from src.lessons.crud import LessonCrud
from src.lessons.shemas import LessonBase

router = APIRouter(prefix='/lesson', tags=['Страница уроков курса'])


@router.get('/{course_id}', summary='Все уроки курса')
def get_all_lessons_current_course(
        course_id: int,
        lesson_crud: LessonCrud = Depends(),
):
    """Получить все уроки курса по его id."""
    return lesson_crud.get_all_course_lessons(course_id)


@router.get('/{course_id}/{lessons_id}', dependencies=[Depends(JWTBearer())],)
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
    return lesson_crud.get_lesson_from_course(course_id, lessons_id, permission.user_email)


@router.post('/{course_id}', status_code=201, dependencies=[Depends(JWTBearer())],)
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


@router.post('/pass/{lessons_id}', dependencies=[Depends(JWTBearer())],)
def pass_lesson(
        lessons_id: int,
        lesson_crud: LessonCrud = Depends(),
        permission: UserPermission = Depends(get_permission)
):
    """
    Делает пометку в бд, что студент прошел данный урок и текущего курса.
    Обновляет время прохождения урока.
    """
    return lesson_crud.get_lesson_from_course(lessons_id, permission.user_email)
