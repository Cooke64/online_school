from starlette import status
from starlette.testclient import TestClient

from tests.utils.users import UserHeaders

endpoints_for_all = {
    '/',
    '/course',
    '/course/1',
    '/lesson/1',
    '/lesson/1/1',
    '/teachers',
    'awards/all_awards/'
}

endpoints_for_student = {
    '/user/me',
    '/student/my_courses',
    '/student/passed_lessons',
    '/student/favorite_lessons',
    '/student/favorite_courses',
    'poll/lesson_poll/{lesson_id}'
}

endpoints_for_teacher = {
    '/user/me',
    '/teachers/pofile'
}


def test_smoke_unathorized(client: TestClient, get_fake_db):
    for url in endpoints_for_all:
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK, f'Ошибка в эндпоинте {url}'


def test_smoke_student(client: TestClient, get_fake_db,
                       auth_student: UserHeaders):
    headers = auth_student.user_1
    urls = endpoints_for_all | endpoints_for_student
    for url in urls:
        response = client.get(url, headers=headers)
        assert response.status_code == status.HTTP_200_OK, f'Ошибка в эндпоинте {url}'


def test_smoke_teacher(client: TestClient, get_fake_db,
                       auth_teacher: UserHeaders):
    headers = auth_teacher.user_1
    urls = endpoints_for_all | endpoints_for_student | endpoints_for_teacher
    for url in urls:
        response = client.get(url, headers=headers)
        assert response.status_code == status.HTTP_200_OK, f'Ошибка в эндпоинте {url}'
