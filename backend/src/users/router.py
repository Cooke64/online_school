from fastapi import APIRouter, Body, Depends

from src.auth.utils.create_jwt import create_jwt
from .crud import UserCrud
from .shemas import UserCreate

router = APIRouter(prefix='/user', tags=['Пользователи'])


@router.get('/')
def get_user_page():
    return {"access_token": 123, "token_type": "bearer"}


@router.get('/login')
def login_user():
    return {"access_token": 123, "token_type": "bearer"}


@router.post('/sign_up')
def sign_up_user(user: UserCreate = Body(
    ..., description="Данные пользователя при регистрации."
), user_crud: UserCrud = Depends()):
    user_crud.create_student_user(user)
    return create_jwt(user.email)


def check_user():
    pass
