from tests.utils.users import UserHeaders

poll = {
    "poll_description": "string"
}
question = {
    "question_text": "string",
    "required_to_correct": 0
}

answers_list = {
    "answers_list": [
        {
            "answer_text": "string",
            "is_correct": True
        }
    ]
}


def test_crud_poll(client, get_fake_db, auth_teacher: UserHeaders):
    response = client.post(
        '/poll/create_poll/1/1/',
        json=poll,
        headers=auth_teacher.user_1
    )
    assert response.status_code == 200, 'Опрос не создан, ошибка с ответом'
    response = client.post(
        '/poll/create_poll/1/1/',
        json=poll.update({'foo': 'bar'}),
        headers=auth_teacher.user_1)
    assert response.status_code == 422
    response = client.post(
        '/poll/create_poll/1/99/',
        json=poll,
        headers=auth_teacher.user_1)
    assert response.status_code == 404
    response = client.delete('/poll/remove_poll/1/1/',
                             headers=auth_teacher.user_1)
    assert response.status_code == 204
    response = client.delete('/poll/remove_poll/1/99/',
                             headers=auth_teacher.user_1)
    assert response.status_code == 404


def test_add_poll_unathorized(client, get_fake_db):
    response = client.post(
        '/poll/create_poll/1/1/',
        json=poll,
    )
    assert response.status_code == 403


def test_question_poll_crud(client, get_fake_db, auth_teacher: UserHeaders):
    # Добавление вопроса к опросу, который существует
    response = client.post(
        '/poll/add_question/1',
        json=question,
        headers=auth_teacher.user_1
    )
    assert response.status_code == 200
    # Добавление вопроса к опросу, которого не существует
    response = client.post(
        '/poll/add_question/999',
        json=question,
        headers=auth_teacher.user_1
    )
    assert response.status_code == 404


def test_add_question_unathorized(client, get_fake_db):
    response = client.post('/poll/add_question/1', json=question)
    assert response.status_code == 403


def test_add_wrong_data_to_question(client, get_fake_db):
    response = client.post(
        '/poll/add_question/1',
        json=question.update({'foo': 'baz'})
    )
    assert response.status_code == 422


def test_answer_poll_crud(client, get_fake_db, auth_teacher: UserHeaders):
    # Добавление ответа к опросу, который существует
    response = client.post(
        '/poll/add_answers/1/1',
        json=answers_list,
        headers=auth_teacher.user_1
    )
    assert response.status_code == 201
    # Добавление ответа к опросу, которого не существует
    response = client.post(
        '/poll/add_answers/1/999',
        json=answers_list,
        headers=auth_teacher.user_1
    )
    assert response.status_code == 404
    # Добавление ответа к опросу не автором урока/курса
    response = client.post(
        '/poll/add_answers/1/1',
        json=answers_list,
        headers=auth_teacher.user_2
    )
    assert response.status_code == 403


def test_answer_poll_not_teacher(client, get_fake_db, auth_student):
    response = client.post(
        '/poll/add_answers/1/1',
        json=answers_list,
        headers=auth_student.user_1
    )
    assert response.status_code == 403
    response = client.post(
        '/poll/add_answers/1/1',
        json=answers_list,
    )
    assert response.status_code == 403


def test_add_wrong_data_to_answer(client, get_fake_db):
    response = client.post(
        '/poll/add_question/1',
        json=answers_list.update({'foo': 'baz'})
    )
    assert response.status_code == 422
