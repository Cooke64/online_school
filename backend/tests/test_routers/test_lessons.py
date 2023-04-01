from tests.utils.users import UserHeaders

data = {
    'title': 'title',
    'description': 'description',
}

lesson = {
    "title": "string",
    "content": "string"
}


def test_course_lessons(client, get_fake_db):
    resp = client.get('/lesson/3')
    assert resp.status_code == 200
    resp = client.get('/lesson/12')
    assert resp.status_code == 404


def test_add_lesson_to_course(client, get_fake_db, auth_teacher: UserHeaders):
    r = client.get('/course/1')
    assert len(r.json().get('course').get('lessons')) == 0
    response = client.post(
        '/lesson/1', json=lesson, headers=auth_teacher.user_1
    )
    assert response.status_code == 201
    r = client.get('/course/1')
    assert len(r.json().get('course').get('lessons')) == 1
    response = client.post('/lesson/1/', json=lesson)
    assert response.status_code == 403
    response = client.post(
        '/lesson/1', json=lesson, headers=auth_teacher.user_2
    )
    assert response.status_code == 403


def test_open_free_lesson(client, get_fake_db, auth_student):
    response = client.get(
        '/lesson/3/1', headers=auth_student.user_1
    )
    assert response.status_code == 200


def test_not_free_lesson(client, get_fake_db, auth_student):
    response = client.get('/lesson/4/1')
    assert response.status_code == 403
