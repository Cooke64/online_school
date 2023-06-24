from fastapi import APIRouter, Depends, Path
from starlette import status

from src.students_awards.awards_crud import AwardCrud
from src.students_awards.shemas import AwardCreate

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
    status_code=status.HTTP_201_CREATED,
)
def create_awards(
        award_data: AwardCreate,
        award_crud: AwardCrud = Depends()):
    return award_crud.create_new_awward(award_data)


@router.delete(
    '/remove/{course_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Удаление награды.'
)
def remove_award(
        award_id: int = Path(
            ...,
            description='id награды, которую надо удалить'
        ),
        award_crud: AwardCrud = Depends(),
):
    return award_crud.remove_award(award_id)
