from fastapi import APIRouter, Depends, Path

from .crud import TeachersCrud, TeacherProfileCrud
from .shemas import TeacherShow, TeacherShowDetail

router = APIRouter(prefix='/teachers', tags=['Преподаватели'])


@router.get('/', response_model=list[TeacherShow])
def get_teacher_list(
        teachers_crud: TeachersCrud = Depends(),
):
    return teachers_crud.get_teachers_data()


@router.get('/profile')
def get_teacher_profile_page(
        teachers_crud: TeacherProfileCrud = Depends(),
):
    """
    Информация для преподавателя о статистике его курсов и его учеников.
        - Список курса преподавателя;
        - Количество комментариев к его курсам;
        - Общий рейтинг его курсов;
        - Количество купленных курсов;
        - Процент прохождения курсов пользователями.
    """
    return teachers_crud.get_teacher_profile()


@router.get('/{teacher_id}', response_model=TeacherShowDetail)
def get_teacher_list(
        teacher_id: int = Path(..., gt=0),
        teachers_crud: TeachersCrud = Depends(),
):
    """Отображает список курсов преподавателя по его id."""
    return teachers_crud.get_teacher_detail(teacher_id)
