from P1_flask_crud_api.models import db, User
from unittest.mock import patch
from sqlalchemy.exc import IntegrityError

def test_post_user(client_empty):
    response = client_empty.post('/users', json={'name':'Alice', 'email':'alice@example.com'})
    assert response.status_code == 201
    data = response.get_json()
    assert isinstance(data, dict)
    assert len(data) == 2
    assert data['message'] == 'User added!'
    user_id = data['id']
    user = db.session.get(User, user_id)
    assert user is not None
    assert user.name == 'Alice'
    assert user.email == 'alice@example.com'

def test_post_user_no_name(client_empty):
    response = client_empty.post('/users', json={'name': '', 'email': 'alice@example.com'})
    assert response.status_code == 400
    data = response.get_json()
    assert isinstance(data, dict)
    assert len(data) == 1
    assert data['error'] == 'Missing name or email.'

def test_post_user_no_email(client_empty):
    response = client_empty.post('/users', json={'name': 'Alice', 'email': ''})
    assert response.status_code == 400
    data = response.get_json()
    assert isinstance(data, dict)
    assert len(data) == 1
    assert data['error'] == 'Missing name or email.'

def test_post_user_email_in_db(client):
    response = client.post('/users', json={'name': 'Alice A', 'email': 'alice@example.com'})
    assert response.status_code == 409
    data = response.get_json()
    assert isinstance(data, dict)
    assert len(data) == 1
    assert data['error'] == 'E-mail already exists!'

def test_post_user_name_in_db(client):
    response = client.post('/users', json={'name': 'Alice', 'email': 'alice_12@example.com'})
    assert response.status_code == 201
    data = response.get_json()
    assert isinstance(data, dict)
    assert len(data) == 2
    assert data['message'] == 'User added!'
    user_id = data['id']
    user = db.session.get(User, user_id)
    assert user is not None
    assert user.name == 'Alice'
    assert user.email == 'alice_12@example.com'

def test_post_user_integrity_error(client_empty):
    fake_exception = IntegrityError(statement="INSERT INTO ...", params={}, orig=Exception("Integrity violation"))
    with patch('P1_flask_crud_api.routes.db.session.commit', side_effect=fake_exception):
        response = client_empty.post('/users', json={'name': 'Alice', 'email': 'alice@example.com'})
        assert response.status_code == 500
        data = response.get_json()
        assert data['error'] == 'Database integrity error'