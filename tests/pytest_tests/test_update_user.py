import pytest
from app.models import db, User

def test_update_existing_user(client):
    with client.application.app_context():
        user = User(name='Gus', email='gus@example.com')
        db.session.add(user)
        db.session.commit()
        user_id = user.id

    payload = {'name': 'Gus Gustafsson', 'email': 'gus123@example.com'}
    expected = {'message': f'User updated successfully!',
                'user': {
                    'id': user_id,
                    'name': payload['name'],
                    'email': payload['email']
                    }
                }

    response = client.put(f'/users/{user_id}', json= payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data == expected

def test_update_non_existing_user_returns_404(client):
    payload = {'name': 'Ian', 'email': 'ian@gmail.com'}
    expected = {'error': 'User not found!'}

    response = client.put('/users/9999', json=payload)
    assert response.status_code == 404
    data = response.get_json()
    assert data == expected

def test_update_with_duplicate_email_returns_409(client):
    with client.application.app_context():
        user1 = User(name='Jane D', email='jane@example.com')
        user2 = User(name='Jane Doe', email='jane_d@example.com')
        db.session.add_all([user1, user2])
        db.session.commit()
        user1_id = user1.id

    payload = {'name': 'Jane D', 'email': 'jane_d@example.com'}
    expected = {'error': 'E-mail already exists.'}

    response = client.put(f'/users/{user1_id}', json=payload)
    assert response.status_code == 409
    data = response.get_json()
    assert data == expected

def test_update_user_same_email_is_ok(client):
    with client.application.app_context():
        user = User(name='Jim', email='jim@example.com')
        db.session.add(user); db.session.commit()
        user_id = user.id

    payload = {'name': 'Jim New', 'email': 'jim@example.com'}
    resp = client.put(f'/users/{user_id}', json=payload)
    assert resp.status_code == 200
    body = resp.get_json()
    assert body['user']['id'] == user_id
    assert body['user']['email'] == 'jim@example.com'

@pytest.mark.parametrize('payload, status, expected', [
    ({'name': '', 'email': 'helen123@example.com'}, 400, {'error': 'Missing name or e-mail.'}),
    ({'name': 'Helen H', 'email': ''}, 400, {'error': 'Missing name or e-mail.'})
])
def test_update_user_payload_errors_400(client, payload, status, expected):
    with client.application.app_context():
        user = User(name='Helen', email='helen@example.com')
        db.session.add(user)
        db.session.commit()
        user_id = user.id

    response = client.put(f'/users/{user_id}', json=payload)
    assert response.status_code == status
    data = response.get_json()
    assert data == expected