user_data = {
    "username": "user",
    "first_name": "firstname",
    "last_name": "last_name",
    "email": '1@1.ru',
    "password": "1",
    "phone": "1"
}

data_to_enter = {
    "email": '1@1.ru',
    "password": "1",
}

data_to_enter_inactive = {
    "email": '2@2.ru',
    "password": "2",
}
wrong_user = {
    "username": "123",
    "first_name": "1234",
}


def test_create_user(client):
    response = client.post('/user/sign_up/student', json=user_data)
    assert response.status_code == 200
    response = client.post('/user/login', json=data_to_enter)
    assert response.status_code == 200


def test_wrong_data_create_user(client):
    response = client.post("/user/sign_up/user", data=wrong_user)
    assert response.status_code == 422


def test_wrong_login_user(client):
    response = client.post('/user/login', json=data_to_enter)
    assert response.status_code == 404


def test_my_page(client, get_fake_db):
    response = client.post('/user/login', json=data_to_enter)
    assert response.status_code == 200
    response = client.get('/user/me', headers=response.json())
    assert response.json()["email"] == data_to_enter.get('email')
    assert response.json()["role"] == 'teacher'


def test_inactive_user_enter_to_me(client, get_fake_db):
    headers = client.post('/user/login', json=data_to_enter_inactive).json()
    response = client.get('/user/me', headers=headers)
    assert response.status_code == 403


def test_make_user_active(client):
    """Проверка, что новый пользователь регистрируется на сайте
        - попытка зайти в профиль неактивному пользователю после авторизации
        - отправка кода подтверждения и активации
        - авторизация и успешный заход в личный кабинет пользователя
    """
    response = client.post('/user/sign_up/student', json=user_data)
    code = response.json().get("code")
    response = client.post('/user/login', json=data_to_enter)
    response = client.get('/user/me', headers=response.json())
    assert response.status_code == 403
    client.get(f'/user/verify_user/{code}')
    response = client.post('/user/login', json=data_to_enter)
    response = client.get('/user/me', headers=response.json())
    assert response.status_code == 200
    assert response.json()["username"] == user_data.get('username')
