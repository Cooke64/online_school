from enum import Enum

from fastapi import APIRouter, Body, Depends, Path
from starlette.responses import RedirectResponse

from .crud import UserCrud
from .models import User
from .shemas import (
    UserCreate,
    UserCreateShowResult,
    UserLogin,
    UserShowProfile
)
from ..auth.utils.auth_bearer import get_current_user, \
    get_permission, UserPermission
from ..auth.utils.create_jwt import create_jwt
from ..auth.utils.hasher import verify_password
from ..exceptions import NotFound, BadRequest

router = APIRouter(prefix='/user', tags=['Пользователи'])


@router.get(
    '/me',
    response_model=UserShowProfile,
    summary='Страница данных о пользователе',
)
def get_user_page(

        permission: UserPermission = Depends(get_permission),
        user_crud: UserCrud = Depends()
):
    """Данные о пользователе. Данные о студенет/преподавателе
    выводятся через отдельный эндпоинт"""
    return user_crud.get_user(permission.user_email)


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


class UserType(str, Enum):
    student = "student"
    teacher = "teacher"


@router.post('/sign_up/{user_type}', response_model=UserCreateShowResult,
             summary='Регистрация')
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
    if user_crud.get_user_by_email(User, user.email):
        raise BadRequest
    user = user_crud.create_user(user_type, user)
    return user


@router.post('/login', summary='Авторизация пользователя')
def login_user(
        form_data: UserLogin,
        user_crud: UserCrud = Depends(),
):
    user = user_crud.get_user(form_data.email)
    if not user or not verify_password(form_data.password, user.password):
        raise NotFound
    access_token = create_jwt(data={"sub": user.email})
    headers = {'Authorization': f'Bearer {access_token}'}
    return headers
