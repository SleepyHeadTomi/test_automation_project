from app.models import db, User

def test_get_users_populated_db(client):
    with client.application.app_context():
        user1 = User(name='Anna', email='anna@example.com')
        user2 = User(name='Bob', email='bob@example.com')
        db.session.add_all([user1, user2])
        db.session.commit()
        expected = [user1.to_dict(), user2.to_dict()]

    response = client.get('/users')
    assert response.status_code == 200

    data = response.get_json()
    assert data == expected

def test_get_users_empty_db(client):
    response = client.get('/users')
    assert response.status_code == 200

    data = response.get_json()
    assert len(data) == 0

def test_get_user(client):
    with client.application.app_context():
        user = User(name='Charlie', email='charlie@example.com')
        db.session.add(user)
        db.session.commit()
        expected = user.to_dict()

    response = client.get(f'/users/{expected['id']}')
    assert response.status_code == 200

    data = response.get_json()
    assert data == expected

def test_get_user_false_id(client):
    response = client.get('/users/9999')
    assert response.status_code == 404

    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'User not found!'