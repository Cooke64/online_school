from fastapi import APIRouter, Depends

from src.students.crud import StudentCrud
from src.students.shemas import ShowUserProfile

router = APIRouter(prefix='/student', tags=['Данные о студенте'])


@router.get('/me', response_model=ShowUserProfile,
            response_model_exclude_unset=True
            )
def get_all_users_courses(
        email: str, user_crud: StudentCrud = Depends()
):
    """
    Возвращает информацию о пользователе.
    Показывает все курсы, на которые он подписан.
    """
    return user_crud.get_students_courses(email)

