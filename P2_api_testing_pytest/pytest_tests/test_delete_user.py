def test_delete_user(client_with_user_id):
    client_with_user, user_id = client_with_user_id

    response = client_with_user.delete(f'/users/{user_id}')
    assert response.status_code == 200

    data = response.get_json()
    assert 'message' in data
    assert data['message'] == f'User with id {user_id} deleted.'

    check = client_with_user.get(f'/users/{user_id}')
    assert check.status_code == 404


def test_delete_non_existing_user(client_with_user_id):
    client_with_user, user_id = client_with_user_id

    client_with_user.delete(f'/users/{user_id}')

    response = client_with_user.delete(f'/users/{user_id}')
    assert response.status_code == 404

    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'User not found!'