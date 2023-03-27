from fastapi import APIRouter, Depends

from src.lessons.shemas import LessonBase
from src.lessons.crud import LessonCrud

router = APIRouter(prefix='/lesson', tags=['Страница урока конкретного курса'])


@router.get('/')
def get_all_lessons(
                    course_crud: LessonCrud = Depends()):
    return course_crud.get_all_lessons()


@router.post('/{course_id}')
def get_all_courses(course_id: int,
                    lesson_data: LessonBase,
                    course_crud: LessonCrud = Depends()):
    return course_crud.add_lesson_to_course(course_id, lesson_data)
