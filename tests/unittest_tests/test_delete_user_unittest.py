import unittest
from sqlalchemy import select
from app.app import app
from app.models import db, User

class TestDeleteUser(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
        self.client = app.test_client()

        with app.app_context():
            db.create_all()
            user1 = User(name='Alice', email='alice@example.com')
            user2 = User(name='Bob', email='bob@example.com')
            db.session.add_all([user1,user2])
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    # noinspection PyTestUnpassedFixture
    def test_delete_user_successfully(self):
        with app.app_context():
            stmt = select(User)
            users = db.session.scalars(stmt).all()
            user1, user2 = users

        response = self.client.delete(f'/users/{user1.id}')
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], f'User with id {user1.id} deleted.')

        with app.app_context():
            query1 = db.session.get(User, user1.id)
            self.assertEqual(query1, None)

            query2 = db.session.get(User, user2.id)
            self.assertEqual(query2.id, 2)
            self.assertEqual(query2.name, 'Bob')
            self.assertEqual(query2.email, 'bob@example.com')

    def test_delete_nonexisting_user(self):
        with app.app_context():
            stmt = select(User)
            users = db.session.scalars(stmt).all()
            user1, _ = users

        # noinspection PyTestUnpassedFixture
        delete_response = self.client.delete(f'/users/{user1.id}')
        self.assertEqual(delete_response.status_code, 200)

        # noinspection PyTestUnpassedFixture
        response = self.client.delete(f'/users/{user1.id}')
        self.assertEqual(response.status_code, 404)

        data = response.get_json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'User not found!')

        with app.app_context():
            stmt = select(User)
            users = db.session.scalars(stmt).all()
            print("Users left in DB:")
            for u in users:
                print(f'User with id = {u.id}: [{u.name}, {u.email}]')

    def test_delete_user(self):
        # noinspection PyTestUnpassedFixture
        response = self.client.delete(f'/users/{9999}')
        self.assertEqual(response.status_code, 404)

        data = response.get_json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'User not found!')

        with app.app_context():
            stmt = select(User)
            users = db.session.scalars(stmt).all()
            print("Users left in DB:")
            for u in users:
                print(f'User with id = {u.id}: [{u.name}, {u.email}]')