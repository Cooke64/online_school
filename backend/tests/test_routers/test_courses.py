from starlette.testclient import TestClient
from fastapi import status
from tests.utils.users import UserHeaders

data = {
    'title': 'title',
    'description': 'description',
    'is_free': False
}


def test_create_course(client: TestClient, auth_teacher: UserHeaders):
    headers = auth_teacher.user_1
    response = client.post('/course', json=data, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['title'] == 'title'
    response = client.get('/course/1')
    assert response.status_code == status.HTTP_200_OK
    response = client.get('/course/2')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_wrong_course(client: TestClient, get_fake_db):
    response = client.get('/course/1')
    assert response.status_code == status.HTTP_200_OK
    response = client.get('/course/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_not_auth_make_course(client: TestClient):
    response = client.post('/course', json=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_course_list(client: TestClient, auth_teacher):
    for _ in range(3):
        client.post('/course/', json=data, headers=auth_teacher.user_1)
    client.post('/course/', json=data, headers=auth_teacher.user_2)
    response = client.get('/course/')
    assert len(response.json()) == 4


def test_remove_course(client: TestClient, auth_teacher, auth_student):
    for i in range(3):
        client.post('/course/', json=data, headers=auth_teacher.user_1)
    # удаление курса автором
    response = client.delete(f'/course/2', headers=auth_teacher.user_1)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # курс действительно удален
    response = client.get('/course/')
    assert len(response.json()) == 2
    # Удаление курса не авторизованным или не преподавателем курса
    response = client.delete(f'/course/1')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    # Удаление курса, которого не существует
    response = client.delete(f'/course/2', headers=auth_teacher.user_1)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    # удаление курса не автором
    response = client.delete(f'/course/1', headers=auth_teacher.user_2)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    # Удаляет курс авторизованный студент
    response = client.delete(
        '/course/1', headers=auth_student.user_1
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_course(client: TestClient, auth_teacher, auth_student):
    client.post('/course/', json=data, headers=auth_teacher.user_1)
    data_to_update = 'data_to_update'
    new_title = {'title': data_to_update}
    response = client.put(
        '/course/1', json=new_title, headers=auth_teacher.user_1
    )
    assert response.json()['title'] == data_to_update
    assert response.status_code == status.HTTP_202_ACCEPTED
    # обнавление курса не авторизованным
    response = client.put('/course/1', json=new_title)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    # обнавление не существующего курса
    response = client.put('/course/2', json=new_title,
                          headers=auth_teacher.user_1)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    # обнавление не автором курса
    response = client.put('/course/1', json=new_title,
                          headers=auth_teacher.user_2)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    response = client.put(
        '/course/1', json=new_title, headers=auth_student.user_1
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_add_and_buy_course(client: TestClient, auth_student, get_fake_db):
    client.post('/course/add/1', headers=auth_student.user_1)
    response = client.post('/course/add/1/pay', headers=auth_student.user_1)
    assert response.status_code == status.HTTP_201_CREATED
    # В списке курсов студента действительно добавился курса
    response = client.get('/student/my_courses', headers=auth_student.user_1)
    assert len(response.json().get('purchased_courses')) == 1
    response = client.post('/course/add/1')
    assert response.status_code == status.HTTP_403_FORBIDDEN


# Проверить тесты дальше отсюда
def test_remove_course_in_user_list(client: TestClient, auth_student, get_fake_db):
    client.post('/course/add/1', headers=auth_student.user_1)
    response = client.delete('/course/remove/1', headers=auth_student.user_1)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = client.get('/user/me', headers=auth_student.user_1)
    assert len(response.json().get('student').get('courses')) == 0


def test_remove_not_existing_course(client: TestClient, auth_student, get_fake_db):
    client.post('/course/add/1', headers=auth_student.user_1)
    response = client.delete('/course/remove/1', headers=auth_student.user_2)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_add_rating_to_course(client: TestClient, auth_student, get_fake_db):
    response = client.post(
        '/course/2/add_rating?rating=4', headers=auth_student.user_1
    )
    assert response.status_code == status.HTTP_201_CREATED
    response = client.post(
        '/course/2/add_rating?rating=4', headers=auth_student.user_1
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    response = client.post(
        '/course/4/add_rating?rating=4', headers=auth_student.user_1
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_course_rating(client: TestClient, auth_student, get_fake_db):
    client.post(
        '/course/2/add_rating?rating=4', headers=auth_student.user_1
    )
    client.put(
        '/course/2/update_rating?new_rating=5', headers=auth_student.user_1
    )
    resposnse = client.get('/course/2/')
    assert resposnse.json().get('rating') == 5.0
