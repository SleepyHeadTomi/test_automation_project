from app.models import db, User

def test_delete_user(client):
    with client.application.app_context():
        user = User(name='Fran', email='fran@example.com')
        db.session.add(user)
        db.session.commit()
        user_id = user.id

    # Ta bort användaren
    response = client.delete(f'/users/{user_id}')
    assert response.status_code == 200
    data = response.get_json()
    expected = {'message': f'User with id {user_id} deleted.'}
    assert data == expected

    # Användaren finns inte kvar längre
    check = client.get(f'/users/{user_id}')
    assert check.status_code == 404

def test_delete_non_existing_user_returns_404(client):
    response = client.delete('/users/9999')
    assert response.status_code == 404

    expected ={'error': 'User not found!'}

    data = response.get_json()
    assert data == expected