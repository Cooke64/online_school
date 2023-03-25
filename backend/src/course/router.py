from fastapi import APIRouter, Depends, Path, Body

from src.course.crud import CourseCrud
from src.course.shemas import CreateCourse, CourseShowDetail

router = APIRouter(prefix='/course', tags=['Главная страничка курсов'])


@router.get('/', response_model=list[CourseShowDetail])
def get_all_courses(course_crud: CourseCrud = Depends()):
    return course_crud.get_all_items()


@router.post('/{course_id}')
def add_course_in_users_list(
        course_id: int = Path(..., description='The id of current post'),
        email: str = Body(..., description='The email of current user'),
        course_crud: CourseCrud = Depends()
):
    course_crud.add_course_by_user(course_id, email)
    return {'course': 'added'}


@router.post('/')
def create_course(
        course_data: CreateCourse,
        course_crud: CourseCrud = Depends()
):
    course_crud.create_new_course(course_data)
    return course_data
