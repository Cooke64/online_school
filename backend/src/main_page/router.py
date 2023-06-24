from fastapi import APIRouter, Depends

from src.main_page.crud import MainCrud

router = APIRouter(tags=['Главная страница'])


@router.get('/')
def get_all_users_courses(
        main_crud: MainCrud = Depends()
):
    """
    Возвращает информацию о пользователе.
    Показывает все курсы, на которые он подписан.
    """
    return main_crud.get_main_page_repsonse()
