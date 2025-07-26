import unittest
from unittest.mock import patch
from sqlalchemy.exc import IntegrityError
from P1_flask_crud_api.app import app
from P1_flask_crud_api.models import db, User

class TestPostUser(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
        self.client = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_post_creates_user_successfully(self):
        # noinspection PyTestUnpassedFixture
        response = self.client.post('/users', json={'name': 'Alice', 'email': 'alice@example.com'})
        self.assertEqual(response.status_code, 201)

        data = response.get_json()
        self.assertIn('message', data)
        self.assertIn('id', data)
        self.assertEqual(data['message'], 'User added!')

        user_id = data['id']

        with app.app_context():
            user = db.session.get(User, user_id)
            self.assertEqual(user.name, 'Alice')
            self.assertEqual(user.email, 'alice@example.com')

    def test_post_user_missing_name(self):
        # noinspection PyTestUnpassedFixture
        response = self.client.post('/users', json={'name': '', 'email': 'alice@example.com'})
        self.assertEqual(response.status_code, 400)

        data = response.get_json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Missing name or email.')

    def test_post_user_missing_email(self):
        # noinspection PyTestUnpassedFixture
        response = self.client.post('/users', json={'name': 'Alice', 'email': ''})
        self.assertEqual(response.status_code, 400)

        data = response.get_json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Missing name or email.')

    def test_post_user_duplicate_email(self):
        with app.app_context():
            db.session.add(User(name='Existing User', email='alice@example.com'))
            db.session.commit()

        # noinspection PyTestUnpassedFixture
        response = self.client.post('/users', json={'name': 'Alice Newman', 'email': 'alice@example.com'})
        self.assertEqual(response.status_code, 409)

        data = response.get_json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'E-mail already exists!')

        with app.app_context():
            self.assertEqual(User.query.count(), 1)

    def test_post_user_throw_integrity_error(self):
        fake_exception = IntegrityError(statement="INSERT INTO ...", params={}, orig=Exception("Integrity violation"))
        with patch('P1_flask_crud_api.routes.db.session.commit', side_effect=fake_exception):
            # noinspection PyTestUnpassedFixture
            response = self.client.post('/users', json={'name': 'Alice', 'email': 'alice@example.com'})
            self.assertEqual(response.status_code, 500)

            data = response.get_json()
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'Database integrity error')