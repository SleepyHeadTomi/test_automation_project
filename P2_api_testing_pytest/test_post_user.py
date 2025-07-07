def test_post_user(client_empty):
    response = client_empty.post('/users', json={'name':'Alice', 'email':'alice@example.com'})
    assert response.status_code == 201
    data = response.get_json()
    assert isinstance(data, dict)
    assert len(data) == 2
    assert data['message'] == 'User added!'
    assert data['id'] == 1