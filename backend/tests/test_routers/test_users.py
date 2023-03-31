user_data = {
    "username": "123",
    "first_name": "1234",
    "last_name": "123",
    "email": "ema3il@m2ail.com",
    "password": "passwo2rd",
    "phone": "12345627822"
}

data_to_enter = {
    "email": "ema3il@m2ail.com",
    "password": "passwo2rd",
}
wrong_user = {
    "username": "123",
    "first_name": "1234",
}


def test_create_user(client):
    response = client.post('/user/sign_up/user', json=user_data)
    assert response.status_code == 200
    assert response.json()["email"] == "ema3il@m2ail.com"
    response = client.post('/user/login', json=data_to_enter)
    assert response.status_code == 200


def test_wrong_data_create_user(client):
    response = client.post("/user/sign_up/user", data=wrong_user)
    assert response.status_code == 422


def test_wrong_login_user(client):
    response = client.post('/user/login', json=data_to_enter)
    assert response.status_code == 404
