from fastapi import APIRouter, Depends

from src.course.crud import CourseCrud
from src.course.models import Course
from src.course.shemas import CourseShow, CreateCourse

router = APIRouter(tags=['Главная страничка курсов'])


# @router.get('/', response_model=list[CourseShow])
# def get_all_courses(course_crud: CourseCrud = Depends()):
#     return course_crud.get_all_items()
#
#
# @router.get('/{course_pk}')
# def get_courses_lesons(course_id: int, course_crud: CourseCrud = Depends()):
#     return course_crud.get_course_lessons(course_id)


@router.post('/')
def create_course(
        course_data: CreateCourse,
        course_crud: CourseCrud = Depends()
):
    course_crud.create_new_course(course_data)
    return course_data
