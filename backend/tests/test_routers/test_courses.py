data = {
    'title': 'title',
    'description': 'description',
    'rating': 4
}


def test_create_course(client):
    response = client.post('/course/', json=data)
    assert response.status_code == 200
    assert response.json()['title'] == 'title'


def test_course_by_id(client):
    client.post('/course/', json=data)
    response = client.get('/course/1')
    assert response.status_code == 200
    assert response.json()['title'] == 'title'


def test_wrong_it_course(client):
    client.post('/course/', json=data)
    response = client.get('/course/10')
    assert response.status_code == 404


def test_create_course_list(client):
    for _ in range(3):
        client.post('/course/', json=data)
    response = client.get('/course/')
    assert response.status_code == 200
    assert len(response.json()) == 3
