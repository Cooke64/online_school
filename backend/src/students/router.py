from fastapi import APIRouter, Depends

from src.exceptions import PermissionDenied
from src.students.crud import StudentCrud
from src.students.shemas import ShowStudentData, FavoriteLessons
from src.students_awards.awards_crud import AwardCrud

router = APIRouter(prefix='/student', tags=['Данные о студенте'])


@router.get('/my_courses',
            response_model=ShowStudentData,
            summary='Информация о студенте')
def get_student_info(
        user_crud: StudentCrud = Depends(),
        award_crud: AwardCrud = Depends()
):
    """
        ## Возвращает информацию о пользователе:
         - Приобретенные курсы.
         - Количество уроков, пройденныхъ за день
         - Количество уроков, пройденныхъ за последний месяц
         - Оставленные комментарии
         - Курсы, пройденные **полностью**
         - Награды
    """
    if not award_crud.student:
        raise PermissionDenied
    return user_crud.get_students_courses() | {
        'awards': award_crud.get_student_award()}


@router.get('/passed_lessons', summary='Уроки, котоые прошел студент')
def get_passed_lessons(
        user_crud: StudentCrud = Depends()
):
    """
    Возвращает информацию о пользователе.
    Показывает все курсы, на которые он подписан.
    """
    return user_crud.get_passed_lessons()


@router.get('/favorite_lessons',
            description='Список всех избранных уроков с '
                        'названием курса и краткой информацией об уроке',
            summary='Избранные уроки',
            response_model=list[FavoriteLessons]
            )
def get_favorite_lessons(
        user_crud: StudentCrud = Depends()
):
    return user_crud.get_favorite_lessons()


@router.get('/favorite_courses',
            description='Список всех избранных курсов',
            summary='Избранные курсы')
def get_favorite_courses(
        user_crud: StudentCrud = Depends()
):
    return user_crud.get_favorite_courses()
