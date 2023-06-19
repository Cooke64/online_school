from fastapi import APIRouter, Depends

from src.students.crud import StudentCrud

router = APIRouter(prefix='/student', tags=['Данные о студенте'])


@router.get('/my_courses')
def get_all_users_courses(
        user_crud: StudentCrud = Depends(),
):
    """
    Возвращает информацию о пользователе.
    Показывает все курсы, на которые он подписан.
    """
    return user_crud.get_students_courses()


@router.get('/passed_lessons')
def get_passed_lessons(
        user_crud: StudentCrud = Depends()
):
    """
    Возвращает информацию о пользователе.
    Показывает все курсы, на которые он подписан.
    """
    return user_crud.get_passed_lessons()
