from fastapi import APIRouter, Depends, Path, Body
from fastapi import HTTPException, status

from src.course.crud import CourseCrud
from src.course.shemas import CreateCourse
from src.exceptions import NotFound

router = APIRouter(prefix='/course', tags=['Главная страничка курсов'])


@router.get('/')
def get_all_courses(course_crud: CourseCrud = Depends()):
    return course_crud.get_all_items()


@router.get('/{course_id}')
def get_course_by_id(
        course_id: int = Path(..., description='The id of current post'),
        course_crud: CourseCrud = Depends()
):
    query = course_crud.get_course_by_id(course_id)
    if not query:
        raise NotFound
    return query


@router.post('/{course_id}')
def add_course_in_users_list(
        course_id: int = Path(..., description='The id of current post'),
        email: str = Body(..., description='The email of current user'),
        course_crud: CourseCrud = Depends()
):
    query = course_crud.get_course_by_id(course_id)
    if not query:
        raise NotFound
    course_crud.add_course_by_user(course_id, email)
    return {'course': 'added'}


@router.post('/')
def create_course(
        course_data: CreateCourse,
        course_crud: CourseCrud = Depends()
):
    course_crud.create_new_course(course_data)
    return course_data
