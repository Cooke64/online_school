from tests.utils.create_fake_bd import USER_DATA

user_data = {
  "username": "user",
  "first_name": "firstname",
  "last_name": "last_name",
  "email": '1@mail.ru',
  "password": "1234567",
  "phone": "12345678"
}

data_to_enter = {
    "email": '1@mail.ru',
    "password": "1234567",
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
    assert response.json()["email"] == data_to_enter.get('email')
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


def test_inactive_user(client, get_fake_db):
    response = client.post('/user/login', json=data_to_enter_inactive)
    response = client.get('/user/me', headers=response.json())
    assert response.status_code == 403
