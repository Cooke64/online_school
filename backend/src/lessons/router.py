from fastapi import APIRouter, Depends, Path
from starlette import status

from src.lessons.crud import LessonCrud
from src.lessons.shemas import LessonBase, CommentBase, ShowLessonDetail

router = APIRouter(prefix='/lesson', tags=['Страница уроков курса'])


@router.get('/{course_id}', summary='Все уроки курса')
def get_all_lessons_current_course(
        course_id: int,
        lesson_crud: LessonCrud = Depends(),
):
    """Получить все уроки курса по его id."""
    return lesson_crud.get_all_course_lessons(course_id)


@router.get('/{course_id}/{lessons_id}', response_model=ShowLessonDetail)
def get_lesson_from_current_course(
        course_id: int,
        lessons_id: int,
        lesson_crud: LessonCrud = Depends(),
):
    """
    Возвращает урок по его id из курса. Если урок платный, или пользователь не получил доступ
    к курсу, то возвращает ответ 403.
    """
    return lesson_crud.get_lesson_from_course(course_id, lessons_id)


@router.post('/{course_id}', status_code=status.HTTP_201_CREATED)
def add_lessons_to_course(
        course_id: int,
        lesson_data: LessonBase,
        lesson_crud: LessonCrud = Depends(),
):
    """
    Добавить курсу по его id новый урок.
    """
    return lesson_crud.add_lesson_to_course(course_id, lesson_data)


@router.post('/pass/{lessons_id}')
def pass_lesson(
        lessons_id: int = Path(..., gt=0),
        lesson_crud: LessonCrud = Depends(),
):
    """
    Делает пометку в бд, что студент прошел данный урок и текущего курса.
    Обновляет время прохождения урока.
    """
    return lesson_crud.make_lessone_done(lessons_id)


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
):
    lesson_crud.add_comment_to_lesson(
        comment_data, lesson_id, course_id)


@router.delete(
    '/{lesson_id}/remove_comment/{comment_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    description='Удалить комментарий уроку по его id.',
    summary='Удалить комментарий'
)
def remove_comment(
        comment_id: int = Path(..., gt=0),
        lesson_id: int = Path(..., gt=0),
        lesson_crud: LessonCrud = Depends(),
):
    lesson_crud.remove_comment_from_lesson(comment_id, lesson_id)


@router.delete(
    '/{course_id}/{lesson_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    description='Удалить урок по его id.',
    summary='Удалить урок'
)
def remove_comment(
        course_id: int = Path(..., gt=0),
        lesson_id: int = Path(..., gt=0),
        lesson_crud: LessonCrud = Depends(),
):
    return lesson_crud.remove_lesson(course_id, lesson_id)
