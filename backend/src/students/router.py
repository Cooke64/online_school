from fastapi import APIRouter, Depends, Path

from src.course.crud import CourseCrud
from src.students.crud import StudentCrud

router = APIRouter(prefix='/student', tags=['Данные о студенте'])


@router.get('/me')
def get_all_users_courses(
        email: str, user_crud: StudentCrud = Depends()
):
    return user_crud.get_students_courses(email)

