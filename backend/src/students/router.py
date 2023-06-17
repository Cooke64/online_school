from fastapi import APIRouter, Depends

from src.auth.utils.auth_bearer import UserPermission, get_permission
from src.exceptions import NotFound
from src.students.crud import StudentCrud
from src.students_awards.awards_crud import AwardCrud
from src.users.models import User

router = APIRouter(prefix='/student', tags=['Данные о студенте'])


@router.get('/my_courses')
def get_all_users_courses(
        permission: UserPermission = Depends(get_permission),
        user_crud: StudentCrud = Depends(),
        awards: AwardCrud = Depends()
):
    """
    Возвращает информацию о пользователе.
    Показывает все курсы, на которые он подписан.
    """
    return user_crud.get_students_courses(permission)


@router.get('/passed_lessons')
def get_all_users_courses(
        permission: UserPermission = Depends(get_permission),
        user_crud: StudentCrud = Depends()
):
    """
    Возвращает информацию о пользователе.
    Показывает все курсы, на которые он подписан.
    """
    user = user_crud.get_user_by_email(User, permission.user_email)
    if not user:
        raise NotFound
    passsed_today, last_month = user_crud.get_lessons_passed_today(user.student.id)
    return {
        'pass_lessons_today': passsed_today,
        'pass_lessons_last_month': last_month,
    }
