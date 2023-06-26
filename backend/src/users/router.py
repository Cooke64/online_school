from fastapi import APIRouter, Body, Depends, Path, UploadFile, File
from starlette.background import BackgroundTasks
from starlette.responses import RedirectResponse

from .crud import UserCrud, UserType
from .shemas import (
    UserCreate,
    UserCreateShowResult,
    UserLogin,
    UserShowProfile
)
from ..auth.utils.auth_bearer import get_current_user
from ..lesson_files.utils.create_file import upload_user_pic
from ..students_awards.awards_crud import AwardCrud

router = APIRouter(prefix='/user', tags=['Пользователи'])


@router.get(
    '/me',
    response_model=UserShowProfile,
    summary='Страница данных о пользователе',
)
def get_user_page(
        task: BackgroundTasks,
        user_crud: UserCrud = Depends(),
        award_crud: AwardCrud = Depends()):
    """Данные о пользователе. Данные о студенет/преподавателе
    выводятся через отдельный эндпоинт"""
    task.add_task(
        award_crud.create_student_award,
    )
    return user_crud.get_user()


@router.get(
    '/verify_user/{link}',
    status_code=302,
    summary='Верификация пользователя'
)
def verify_new_user(
        link: str = Path(...),
        email=Depends(get_current_user),
        user_crud: UserCrud = Depends()
):
    """Верификация пользователя. Пользователь должен быть авторизован.
    При успешной авторизации редирект на страницу с курсами.
    """
    user_crud.verify_user(email, link)
    return RedirectResponse('/course')


@router.post(
    '/sign_up/{user_type}',
    response_model=UserCreateShowResult,
    summary='Регистрация нового пользователя'
)
def sign_up_user(user: UserCreate = Body(
    ..., description="Данные пользователя при регистрации."),
        *,
        user_type: UserType,
        user_crud: UserCrud = Depends()):
    """
    Создание нового пользователя, добаляет в бд нового пользователя с ролью Student.
    Создает запись в модели Student. Поле is_active = False.
    first_name, last_name, username необязательные поля
    пользователь должен указать номер телефона. Номер телефона должен быть уникальным
    """
    return user_crud.create_user(user_type, user)


@router.post('/login', summary='Авторизация пользователя')
def login_user(
        form_data: UserLogin,
        user_crud: UserCrud = Depends(),
):
    return user_crud.login_user(form_data)


@router.post(
    '/upload_user_pic',
    summary='Загрузка аватара для пользователя',
)
def create_user_profile_image(
        task: BackgroundTasks,
        photo: UploadFile = File(...),
        user_crud: UserCrud = Depends()
):
    task.add_task(
        upload_user_pic,
        file_obj=photo,
        user_crud=user_crud
    )
    return user_crud.get_json_reposnse('Успешно загружен', 201)
