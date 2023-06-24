from fastapi import APIRouter, Depends

from src.students_awards.awards_crud import AwardCrud

router = APIRouter(prefix='/awards', tags=['Награды'])


@router.get(
    '/all_awards',
    summary='Список всех наград',
)
def create_awards(
        award_crud: AwardCrud = Depends()):
    return award_crud.get_all_awards()


@router.post(
    '/create_award',
    summary='Создание награды для пользователей',
)
def create_awards(
        award_data,
        award_crud: AwardCrud = Depends()):
    return award_crud.create_new_awward(award_data)


