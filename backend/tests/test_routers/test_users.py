user_data = {
  "username": "user",
  "first_name": "firstname",
  "last_name": "last_name",
  "email": "email@mail.com",
  "password": "password",
  "phone": "12345678"
}

data_to_enter = {
    "email": "email@mail.com",
    "password": "password",
}
wrong_user = {
    "username": "123",
    "first_name": "1234",
}


def test_create_user(client):
    response = client.post('/user/sign_up/student', json=user_data)
    assert response.status_code == 200
    assert response.json()["email"] == "email@mail.com"
    response = client.post('/user/login', json=data_to_enter)
    assert response.status_code == 200


def test_wrong_data_create_user(client):
    response = client.post("/user/sign_up/user", data=wrong_user)
    assert response.status_code == 422


def test_wrong_login_user(client):
    response = client.post('/user/login', json=data_to_enter)
    assert response.status_code == 404
