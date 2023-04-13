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
    d = {
        'popular':main_crud.get_three_popular(),
        'rating': main_crud.get_three_withmax_raiting(),
        'top_free': main_crud.top_free()
    }
    return d
