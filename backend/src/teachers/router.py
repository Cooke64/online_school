from fastapi import APIRouter, Depends, Path

from .crud import TeachersCrud
from .shemas import TeacherShow, TeacherShowDetail

router = APIRouter(prefix='/teachers', tags=['Преподаватели'])


@router.get('/', response_model=list[TeacherShow])
def get_teacher_list(
        teachers_crud: TeachersCrud = Depends(),
):
    return teachers_crud.get_teachers_data()


@router.get('/{teacher_id}', response_model=TeacherShowDetail)
def get_teacher_list(
        teacher_id: int = Path(..., gt=0),
        teachers_crud: TeachersCrud = Depends(),
):
    return teachers_crud.get_teacher_detail(teacher_id)
