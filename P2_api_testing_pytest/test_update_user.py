from http.client import responses


def test_update_existing_user(client_with_user_id):
    client_with_user, user_id = client_with_user_id

    updated_user = {'name': 'Alice Newman', 'email': 'alice.newman@example.com'}
    response = client_with_user.put(f'/users/{user_id}', json=updated_user)
    assert response.status_code == 200

    data = response.get_json()
    assert 'message' in data
    assert 'user' in data

    assert data['message'] == 'User updated successfully!'
    assert data['user']['id'] == user_id
    assert data['user']['name'] == updated_user['name']
    assert data['user']['email'] == updated_user['email']

def test_non_existing_user(client_with_user_id):
    client_with_user, _ = client_with_user_id

    update_values = {'name': 'Jane Doe', 'email': 'jane.doe@gmail.com'}

    response = client_with_user.put('/users/9999', json=update_values)
    assert response.status_code == 404

    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'User not found!'

def test_email_restriction(client_with_user_id2):
    client_with_user, user1_id, user2_id = client_with_user_id2

    update_values = {'name': 'Alice', 'email': 'alice.newman@example.com'}

    response = client_with_user.put(f'/users/{user1_id}', json=update_values)
    assert response.status_code == 409

    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'E-mail already exists.'

    check_user = client_with_user.get(f'/users/{user1_id}')
    user_data = check_user.get_json()
    assert user_data['email'] != update_values['email']

def test_update_missing_name_value(client_with_user_id):
    client_with_user, user_id = client_with_user_id

    update_values = {'name': '', 'email': 'alice.newman@gmail.com'}

    response = client_with_user.put(f'/users/{user_id}', json=update_values)
    assert response.status_code == 400

    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Missing name or e-mail.'

def test_update_missing_email_value(client_with_user_id):
    client_with_user, user_id = client_with_user_id

    update_values = {'name': 'Alice Newman', 'email': ''}

    response = client_with_user.put(f'/users/{user_id}', json=update_values)
    assert response.status_code == 400

    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Missing name or e-mail.'