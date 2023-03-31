from tests.utils.users import UserHeaders

data = {
    'title': 'title',
    'description': 'description',
    'rating': 4
}


def test_create_course(client, auth_teacher: UserHeaders):
    response = client.post('/course', json=data, headers=auth_teacher.user_1)
    assert response.status_code == 201
    assert response.json()['title'] == 'title'


def test_get_course_by_id(client, auth_teacher):
    client.post('/course', json=data, headers=auth_teacher.user_1)
    response = client.get('/course/1')
    assert response.status_code == 200
    assert response.json()['title'] == 'title'


def test_not_auth_make_course(client):
    response = client.post('/course', json=data)
    assert response.status_code == 403


def test_create_course_list(client, auth_teacher):
    for _ in range(3):
        client.post('/course/', json=data, headers=auth_teacher.user_1)
    client.post('/course/', json=data, headers=auth_teacher.user_2)
    response = client.get('/course/')
    assert response.status_code == 201
    assert len(response.json()) == 4


def test_remove_course(client, auth_teacher, auth_student):
    for i in range(3):
        client.post('/course/', json=data, headers=auth_teacher.user_1)
    # удаление курса автором
    response = client.delete(f'/course/2', headers=auth_teacher.user_1)
    assert response.status_code == 204
    # курс действительно удален
    response = client.get('/course/')
    assert len(response.json()) == 2
    # Удаление курса не авторизованным или не преподавателем курса
    response = client.delete(f'/course/1')
    assert response.status_code == 403
    # Удаление курса, которого не существует
    response = client.delete(f'/course/2', headers=auth_teacher.user_1)
    assert response.status_code == 404
    # удаление курса не автором
    response = client.delete(f'/course/1', headers=auth_teacher.user_2)
    assert response.status_code == 403
    # Удаляет курс авторизованный студент
    response = client.delete(
        '/course/1', headers=auth_student.user_1
    )
    assert response.status_code == 403


def test_update_course(client, auth_teacher, auth_student):
    client.post('/course/', json=data, headers=auth_teacher.user_1)
    data_to_update = 'data_to_update'
    new_title = {'title': data_to_update}
    response = client.put(
        '/course/1', json=new_title, headers=auth_teacher.user_1
    )
    assert response.json()['title'] == data_to_update
    assert response.status_code == 202
    # обнавление курса не авторизованным
    response = client.put('/course/1', json=new_title)
    assert response.status_code == 403
    # обнавление не существующего курса
    response = client.put('/course/2', json=new_title,
                          headers=auth_teacher.user_1)
    assert response.status_code == 404
    # обнавление не автором курса
    response = client.put('/course/1', json=new_title,
                          headers=auth_teacher.user_2)
    assert response.status_code == 403
    response = client.put(
        '/course/1', json=new_title, headers=auth_student.user_1
    )
    assert response.status_code == 403


def test_add_course_in_user_list(client, auth_student, get_fake_db):
    response = client.post('/course/add/1', headers=auth_student.user_1)
    assert response.status_code == 201
    # В списке курсов студента действительно добавился курса
    response = client.get('/user/me', headers=auth_student.user_1)
    assert len(response.json().get('student').get('courses')) == 1


def test_remove_course_in_user_list(client, auth_student, get_fake_db):
    client.post('/course/add/1', headers=auth_student.user_1)
    response = client.delete('/course/remove/1', headers=auth_student.user_1)
    assert response.status_code == 204
    response = client.get('/user/me', headers=auth_student.user_1)
    assert len(response.json().get('student').get('courses')) == 0


def test_remove_not_existing_course(client, auth_student, get_fake_db):
    client.post('/course/add/1', headers=auth_student.user_1)
    response = client.delete('/course/remove/1', headers=auth_student.user_2)
    assert response.status_code == 404


def test_add_rating_to_course(client, auth_student, get_fake_db):
    response = client.post(
        '/course/2/add_rating?rating=4', headers=auth_student.user_1
    )
    assert response.status_code == 201
    response = client.post(
        '/course/2/add_rating?rating=4', headers=auth_student.user_1
    )
    assert response.status_code == 400
    response = client.post(
        '/course/4/add_rating?rating=4', headers=auth_student.user_1
    )
    assert response.status_code == 404
    # print(client.get('/course/'))


def test_update_course_rating(client, auth_student, get_fake_db):
    client.post(
        '/course/2/add_rating?rating=4', headers=auth_student.user_1
    )
    client.put(
        '/course/2/update_rating?new_rating=5', headers=auth_student.user_1
    )
    resposnse = client.get('/course/2/')
    assert resposnse.json().get('rating') == 5.0
