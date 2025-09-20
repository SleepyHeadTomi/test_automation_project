import pytest
from app.models import db, User

def test_post_user(client):
    response = client.post('/users', json={'name':'Alice', 'email':'alice@example.com'})
    assert response.status_code == 201

    data = response.get_json()
    assert data == {'message': 'User added!', 'id': data['id']}

    user = db.session.get(User, data['id'])
    assert user is not None

@pytest.mark.parametrize('payload, status, expected', [
    ({'name': '', 'email': 'debbie@example.com'}, 400, {'error': 'Missing name or e-mail.'}),
    ({'name': 'Debbie', 'email': ''}, 400, {'error': 'Missing name or e-mail.'})
])

def test_post_user_payload_errors(client, payload, status, expected):
    response = client.post('/users', json=payload)
    assert response.status_code == status

    data = response.get_json()
    assert data == expected

def test_post_user_duplicate_email_returns_409(client):
    with client.application.app_context():
        ref_user = User(name='Eric', email='eric@example.com')
        db.session.add(ref_user)
        db.session.commit()

    expected = {'error': 'E-mail already exists!'}

    response = client.post('/users', json={'name': 'Eric A', 'email': 'eric@example.com'})
    assert response.status_code == 409

    data = response.get_json()
    assert data == expected