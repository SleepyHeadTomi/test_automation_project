import pytest
from app import create_app
from app.models import db

@pytest.fixture
def client():
    app = create_app('sqlite:///:memory:')
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()