import unittest
from P1_flask_crud_api.app import app
from P1_flask_crud_api.models import db, User

class TestGetUsers(unittest.TestCase):
    def setUp(self):
        app.config['Testing'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
        self.client = app.test_client()

        with app.app_context():
            db.create_all()
            user1 = User(name='Alice', email='alice@example.com')
            user2 = User(name='Bob', email='bob@example.com')
            db.session.add_all([user1, user2])
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.drop_all()


    def test_get_users(self):
        # noinspection PyTestUnpassedFixture
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(len(data), 2)

        user1 = data[0]
        self.assertEqual(user1['id'], 1)
        self.assertEqual(user1['name'], 'Alice')
        self.assertEqual(user1['email'], 'alice@example.com')

    def test_get_spec_user(self):
        # noinspection PyTestUnpassedFixture
        response = self.client.get('/users/1')
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(len(data), 3)

    def test_get_user_invalid_id(self):
        # noinspection PyTestUnpassedFixture
        response = self.client.get('/users/9999')
        self.assertEqual(response.status_code, 404)

        data = response.get_json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'User not found!')

class TestGetUsersEmptyDB(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
        self.client = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_get_user_empty_db(self):
        # noinspection PyTestUnpassedFixture
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(data, [])