from tests.utils.services import MainResponse as Resp
from tests.utils.users import UserHeaders
from fastapi.testclient import TestClient
from fastapi import status

data = {
    'title': 'title',
    'description': 'description',
}

lesson = {
    "title": "string",
    "content": "string"
}


def test_course_lessons(client: TestClient, get_fake_db):
    resp = Resp(client.get('/lesson/3'))
    resp.assert_status(status.HTTP_200_OK)
    # Получить несуществующий урок курса
    resp = Resp(client.get('/lesson/999'))
    resp.assert_status(status.HTTP_404_NOT_FOUND)


def test_add_lesson_to_course(client: TestClient, get_fake_db, auth_teacher: UserHeaders):
    r = client.get('/course/1')
    assert len(r.json().get('course').get('lessons')) == 0
    response = client.post(
        '/lesson/1', json=lesson, headers=auth_teacher.user_1
    )
    assert response.status_code == status.HTTP_201_CREATED
    r = client.get('/course/1')
    assert len(r.json().get('course').get('lessons')) == 1
    response = client.post('/lesson/1/', json=lesson)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.post(
        '/lesson/1', json=lesson, headers=auth_teacher.user_2
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_open_free_lesson(client: TestClient, get_fake_db, auth_student):
    response = client.get(
        '/lesson/3/1', headers=auth_student.user_1
    )
    assert response.status_code == status.HTTP_200_OK


def test_not_free_lesson(client: TestClient, get_fake_db, auth_student):
    response = client.get('/lesson/4/1')
    assert response.status_code == status.HTTP_403_FORBIDDEN
