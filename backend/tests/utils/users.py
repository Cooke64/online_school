import typing

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.utils.crud import (
    create_user,
    create_teacher,
    create_student
)

Header = dict[str] | None


class UserData(typing.NamedTuple):
    email: str
    username: str
    password: str


class UserHeaders(typing.NamedTuple):
    user_1: dict
    user_2: dict


def get_headers(
        client: TestClient,
        email: str, password: str
) -> Header:
    data = {'email': email, 'password': password}
    response = client.post('/user/login', json=data)
    resp = response.json()
    return resp if resp else {}


def get_teacher_headers(userdata: UserData, client, session) -> Header:
    user = create_user(*userdata, session)
    create_teacher(user.id, session)
    return get_headers(client, userdata.email, userdata.password)


def auth_teachers(client: TestClient, session: Session) -> UserHeaders:
    """
    Создает и авторизует двух преподавателей.
    Возвращает Headers с их валидным токеном.
    """
    t_1 = UserData('1@mail.ru', 'user1', '1234567')
    t_2 = UserData('2@mail.ru', 'user2', '1234567')
    teacher_header_1 = get_teacher_headers(t_1, client, session)
    teacher_header_2 = get_teacher_headers(t_2, client, session)
    return UserHeaders(teacher_header_1, teacher_header_2)


def get_users_headers(userdata: UserData, client, session):
    """ Проверяет, что нет созданного пользователя по email и
    создает его. Возвращает Валидный токен пользователя.
    """
    user = create_user(*userdata, session, is_teacher=False)
    create_student(user.id, session)
    return get_headers(client, userdata.email, userdata.password)


def auth_students(client: TestClient, session: Session) -> UserHeaders:
    """
    Создает и авторизует двух студентов.
    Возвращает UserHeaders с их валидным токеном.
    """
    u_1 = UserData('3@mail.ru', 'user3', '1234567')
    u_2 = UserData('4@mail.ru', 'user4', '1234567')
    user_header_1 = get_users_headers(u_1, client, session)
    user_header_2 = get_users_headers(u_2, client, session)
    return UserHeaders(user_header_1, user_header_2)
