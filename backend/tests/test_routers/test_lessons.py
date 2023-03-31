from tests.utils.users import UserHeaders

data = {
    'title': 'title',
    'description': 'description',
    'rating': 4
}

lesson = {
    "title": "string",
    "content": "string"
}


def test_add_lesson_to_course(client, auth_teacher: UserHeaders):
    response = client.post('/course', json=data, headers=auth_teacher.user_1)
    assert response.status_code == 201
    response = client.post('/lesson/1/', json=lesson, headers=auth_teacher.user_1)
    assert response.status_code == 201
    response = client.get('/course/1')
    lesson_in_bd = response.json().get('lessons')[0]
    assert lesson_in_bd['title'] == lesson['title']


def add_multiple_lessons(client, auth_teacher: UserHeaders):
    client.post('/course', json=data, headers=auth_teacher.user_1)
    for _ in range(3):
        client.post('/lesson/1/', json=lesson, headers=auth_teacher.user_1)
    response = client.get('/course/1')
    assert len(response.json().get('lessons')) == 3

