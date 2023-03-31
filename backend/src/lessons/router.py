from fastapi import APIRouter, Depends

from src.lessons.crud import LessonCrud
from src.lessons.shemas import LessonBase

router = APIRouter(prefix='/lesson', tags=['Страница урока конкретного курса'])


@router.get('/{course_id}')
def get_all_lessons_current_course(
        course_id: int,
        lesson_crud: LessonCrud = Depends()):
    return lesson_crud.get_all_course_lessons(course_id)


@router.get('/{course_id}/{lessons_id}')
def get_lesson_from_current_course(
        course_id: int,
        lessons_id: int,
        lesson_crud: LessonCrud = Depends()):
    return lesson_crud.get_lesson_from_course(course_id, lessons_id)


@router.post('/{course_id}', status_code=201)
def add_lessons_to_course(
        course_id: int,
        lesson_data: LessonBase,
        lesson_crud: LessonCrud = Depends()):
    """
    Добавить курсу по его id новый урок.
    """
    return lesson_crud.add_lesson_to_course(course_id, lesson_data)
