from fastapi import APIRouter, Depends

from src.auth.utils.auth_bearer import JWTBearer, get_current_user
from src.students.crud import StudentCrud
from src.students.shemas import ShowUserProfile

router = APIRouter(prefix='/student', tags=['Данные о студенте'])


@router.get('/my_courses')
def get_all_users_courses(
        email=Depends(get_current_user),
        user_crud: StudentCrud = Depends()
):
    """
    Возвращает информацию о пользователе.
    Показывает все курсы, на которые он подписан.
    """
    return user_crud.get_students_courses(email)


@router.get('/liked_courses')
def get_all_users_courses(
        email=Depends(get_current_user),
        user_crud: StudentCrud = Depends()
):
    pass


@router.get('/passed_courses')
def get_all_users_courses(
        email=Depends(get_current_user),
        user_crud: StudentCrud = Depends()
):
    pass


@router.get('/left_comment')
def get_all_users_courses(
        email=Depends(get_current_user),
        user_crud: StudentCrud = Depends()
):
    pass
