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