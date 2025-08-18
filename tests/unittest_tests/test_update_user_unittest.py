import unittest
from sqlalchemy import select
from app.app import app
from app.models import db, User

class TestUpdateUser(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
        self.client = app.test_client()

        with app.app_context():
            db.create_all()
            user = User(name='Alice', email='alice@example.com')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_update_user_successfully(self):
        with app.app_context():
            user = db.session.execute(select(User)).scalars().first()

        # noinspection PyTestUnpassedFixture
        response = self.client.put(f'/users/{user.id}', json={'name': 'Alice Newman', 'email': 'alice_n@example.com'})
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertIn('message', data)
        self.assertIn('user', data)
        self.assertEqual(data['message'], 'User updated successfully!')
        self.assertEqual(data['user']['id'], user.id)
        self.assertEqual(data['user']['name'], 'Alice Newman')
        self.assertEqual(data['user']['email'], 'alice_n@example.com')

    def test_update_non_existing_user(self):
        # noinspection PyTestUnpassedFixture
        response = self.client.put('/users/9999', json={'name': 'Alice Newman', 'email': 'alice_n@example.com'})
        self.assertEqual(response.status_code, 404)

        data = response.get_json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'User not found!')

    def test_update_user_missing_name(self):
        with app.app_context():
            user = db.session.execute(select(User)).scalars().first()
        # noinspection PyTestUnpassedFixture
        response = self.client.put(f'/users/{user.id}', json={'name': '', 'email': 'alice_n@example.com'})
        self.assertEqual(response.status_code, 400)

        data = response.get_json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Missing name or e-mail.')

    def test_update_user_missing_email(self):
        with app.app_context():
            user = db.session.execute(select(User)).scalars().first()
        # noinspection PyTestUnpassedFixture
        response = self.client.put(f'/users/{user.id}', json={'name': 'Alice Newman', 'email': ''})
        self.assertEqual(response.status_code, 400)

        data = response.get_json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Missing name or e-mail.')

    def test_update_user_duplicate_email(self):
        with app.app_context():
            user2 = User(name='Alice Newman', email='alice_nman@example.com')
            db.session.add(user2)
            db.session.commit()
            user2_id = user2.id


        # noinspection PyTestUnpassedFixture
        response = self.client.put(f'/users/{user2_id}', json={'name': 'Alice Newman', 'email': 'alice@example.com'})
        self.assertEqual(response.status_code, 409)

        data = response.get_json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'E-mail already exists.')