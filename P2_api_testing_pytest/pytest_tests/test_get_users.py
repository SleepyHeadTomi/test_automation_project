def test_get_users(client):
    response = client.get('/users')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]['id'] == 1
    assert data[0]['name'] == 'Alice'
    assert data[0]['email'] == 'alice@example.com'

def test_get_users_empty(client_empty):
    response = client_empty.get('/users')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 0

def test_get_user(client):
    response = client.get('/users/1')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert len(data) == 3
    assert data['id'] == 1
    assert data['name'] == 'Alice'
    assert data['email'] == 'alice@example.com'

def test_get_user_false_id(client):
    response = client.get('/users/10')
    assert response.status_code == 404
    data = response.get_json()
    assert isinstance(data, dict)
    assert len(data) == 1
    assert data['error'] == 'User not found!'
