from fastapi import APIRouter, Depends

from src.lessons.crud import LessonCrud
from src.lessons.shemas import LessonBase

router = APIRouter(prefix='/lesson', tags=['Страница урока конкретного курса'])


@router.get('/')
def get_all_lessons(lesson_crud: LessonCrud = Depends()):
    return lesson_crud.get_all_lessons()


@router.post('/{course_id}')
def add_lessons_to_course(
        course_id: int,
        lesson_data: LessonBase,
        lesson_crud: LessonCrud = Depends()):
    """
    Добавить курсу по его id новый урок.
    """
    return lesson_crud.add_lesson_to_course(course_id, lesson_data)
