from fastapi import APIRouter, Body, Depends

from src.auth.utils.create_jwt import create_jwt
from .crud import UserCrud
from .shemas import UserCreate, UserLogin


router = APIRouter(prefix='/user', tags=['Пользователи'])


@router.get('/all_users')
def get_user_page(user_crud: UserCrud = Depends()):
    data = user_crud.get_all_users()
    return data


@router.post('/login')
def login_user(user: UserLogin, user_crud: UserCrud = Depends()):
    if user_crud.get_user(user.email):
        return {"access_token": 123, "token_type": "bearer"}
    return {'no user': 'no user'}


@router.post('/sign_up')
def sign_up_user(user: UserCreate = Body(
    ..., description="Данные пользователя при регистрации."
), user_crud: UserCrud = Depends()):
    """
    Создание нового пользователя, добаляет в бд нового пользователя с ролью Student.
    Создает запись в модели Student. Поле is_active = False.
    first_name, last_name, username необязательные поля
    пользователь должен указать номер телефона. Номер телефона должен быть уникальным
    """
    hashed_password = create_jwt(user.email)
    user_crud.create_student_user(user, hashed_password)
    return hashed_password
