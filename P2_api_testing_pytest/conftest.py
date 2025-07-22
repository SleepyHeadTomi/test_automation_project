import pytest
from P1_flask_crud_api.app import app
from P1_flask_crud_api.models import db, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            user1 = User(name='Alice', email='alice@example.com')
            user2 = User(name='Bob', email='bob@example.com')
            db.session.add_all([user1, user2])
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()

@pytest.fixture
def client_empty():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    with app.test_client() as client_empty:
        with app.app_context():
            db.create_all()
        yield client_empty
        with app.app_context():
            db.drop_all()

@pytest.fixture
def client_with_user_id():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    with app.test_client() as client_with_user:
        with app.app_context():
            db.create_all()
            user = User(name='Alice', email='alice@example.com')
            db.session.add(user)
            db.session.commit()
            yield client_with_user, user.id
        with app.app_context():
            db.drop_all()

@pytest.fixture
def client_with_user_id2():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    with app.test_client() as client_with_user:
        with app.app_context():
            db.create_all()
            user1 = User(name='Alice', email='alice@example.com')
            user2 = User(name='Alice Newman', email='alice.newman@example.com')
            db.session.add_all([user1, user2])
            db.session.commit()
            yield client_with_user, user1.id, user2.id
        with app.app_context():
            db.drop_all()