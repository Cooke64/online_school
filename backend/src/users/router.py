from enum import Enum

from fastapi import APIRouter, Body, Depends

from .crud import UserCrud
from .shemas import UserCreate, UserCreateShowResult, UserLogin, \
    UserShowProfile
from ..auth.utils.auth_bearer import JWTBearer, get_current_user
from ..auth.utils.create_jwt import create_jwt
from ..auth.utils.hasher import verify_password
from ..exceptions import NotFound

router = APIRouter(prefix='/user', tags=['Пользователи'])


@router.get('/me', dependencies=[Depends(JWTBearer())], response_model=UserShowProfile)
def get_user_page(
        email=Depends(get_current_user),
        user_crud: UserCrud = Depends()
):
    """Данные о пользователе. Данные о студенет/преподавателе
    выводятся через отдельный эндпоинт"""
    return user_crud.get_user(email)


class UserType(str, Enum):
    student = "student"
    teacher = "teacher"


@router.post('/sign_up/{user_type}', response_model=UserCreateShowResult)
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
    match user_type:
        case UserType.student.value:
            user = user_crud.create_student_user(user)
        case UserType.teacher.value:
            user = user_crud.create_teacher_user(user)
    return user


@router.post('/login')
def login_user(form_data: UserLogin,
               user_crud: UserCrud = Depends()):
    """Processes user's authentication and returns a token
        on successful authentication.

        request body:

        - email: Unique identifier for a user email,

        - password:
        """
    user = user_crud.get_user(form_data.email)
    if not user or not verify_password(form_data.password, user.password):
        raise NotFound
    access_token = create_jwt(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
