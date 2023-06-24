from fastapi import APIRouter, Depends

from src.students.crud import StudentCrud
from src.students.shemas import ShowStudentData
from src.students_awards.awards_crud import AwardCrud

router = APIRouter(prefix='/student', tags=['Данные о студенте'])


@router.get('/my_courses', response_model=ShowStudentData)
def get_all_users_courses(
        user_crud: StudentCrud = Depends(),
        award_crud: AwardCrud = Depends()
):
    """
    Возвращает информацию о пользователе.
    Показывает все курсы, на которые он подписан.
    """
    award_crud.create_student_award()
    return user_crud.get_students_courses() | {
        'awards': award_crud.get_student_award()}


@router.get('/passed_lessons')
def get_passed_lessons(
        user_crud: StudentCrud = Depends()
):
    """
    Возвращает информацию о пользователе.
    Показывает все курсы, на которые он подписан.
    """
    return user_crud.get_passed_lessons()
