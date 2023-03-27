user_data = {
  "username": "123",
  "first_name": "1234",
  "last_name": "123",
  "email": "ema3il@m2ail.com",
  "password": "passwo2rd",
  "phone": "12345627822"
}

wrong_user = {
    "username": "123",
    "first_name": "1234",
}


def test_create_user(client):
    response = client.post("/user/sign_up", json=user_data)
    assert response.status_code == 200
    assert response.json()["email"] == "ema3il@m2ail.com"


def test_wrong_data_create_user(client):
    response = client.post("/user/sign_up", data=wrong_user)
    assert response.status_code == 422
