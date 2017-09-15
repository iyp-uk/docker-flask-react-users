import json
import datetime
from tests.base import BaseTestCase
from app.api.models import User
from app import db


def add_user(username, email, created_at=datetime.datetime.utcnow()):
    """Adds a single user"""
    user = User(username=username, email=email, created_at=created_at)
    db.session.add(user)
    db.session.commit()
    return user


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_users(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Ensure we can create a new user in the database"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='testuser',
                    email='user@example.com'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('user@example.com was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """Ensure error is thrown when payload is invalid"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict(
                    email='user@example.com'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_empty_payload(self):
        """Ensure error is thrown when payload is empty"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict()),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_user(self):
        """Ensure error is thrown when user already exists"""
        with self.client:
            # first post, we don't mind the response at this point
            self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='testuser',
                    email='user@example.com'
                )),
                content_type='application/json',
            )
            # second post, get the response:
            response = self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='testuser',
                    email='user@example.com'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 409)
            self.assertIn('Sorry. That email already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_get_user(self):
        """Ensure we can get a single user based on its ID"""
        # add a user for this test.
        user = add_user('testuser', 'user@example.com')
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue('created_at' in data['data'])
            self.assertIn('testuser', data['data']['username'])
            self.assertIn('user@example.com', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_get_user_invalid_id(self):
        """Ensures an error is thrown when the user id is not found"""
        user = add_user('testuser', 'user@example.com')
        with self.client:
            response = self.client.get(f'/users/{user.id + 1}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('fail', data['status'])
            self.assertIn('User not found.', data['message'])

    def test_get_user_no_id(self):
        """Ensure an error is thrown when no integer id is specified"""
        with self.client:
            response = self.client.get('/users/invalid')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('fail', data['status'])
            self.assertIn('Invalid request, User id must be integer.', data['message'])

    def test_get_users(self):
        """Ensure we can retrieve all users"""
        created = datetime.datetime.utcnow() + datetime.timedelta(-30)
        add_user('testuser', 'user@example.com')
        add_user('testuser2', 'user2@example.com', created)
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertEqual(len(data['data']['users']), 2)
            self.assertTrue('created_at' in data['data']['users'][0])
            self.assertTrue('created_at' in data['data']['users'][1])
            self.assertIn('testuser', data['data']['users'][0]['username'])
            self.assertIn('user@example.com', data['data']['users'][0]['email'])
            self.assertIn('testuser2', data['data']['users'][1]['username'])
            self.assertIn('user2@example.com', data['data']['users'][1]['email'])

    def test_get_users_html(self):
        """Ensure we can retrieve all users in HTML"""
        add_user('testuser', 'user@example.com')
        add_user('testuser2', 'user2@example.com')
        with self.client:
            response = self.client.get('/users', headers={'Accept': 'text/html'})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<h1>All Users</h1>', response.data)
            self.assertNotIn(b'<p>No users!</p>', response.data)
            self.assertIn(b'<strong>testuser</strong>', response.data)
            self.assertIn(b'<strong>testuser2</strong>', response.data)

    def test_get_users_html_no_users(self):
        """Ensure we get correct response when no users in HTML"""
        with self.client:
            response = self.client.get('/users', headers={'Accept': 'text/html'})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<h1>All Users</h1>', response.data)
            self.assertIn(b'<p>No users!</p>', response.data)

    def test_main_add_user(self):
        """Ensure a new user can be added through the HTML form"""
        with self.client:
            response = self.client.post(
                '/users',
                data=dict(username='testuser', email='user@example.com'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<h1>All Users</h1>', response.data)
            self.assertNotIn(b'<p>No users!</p>', response.data)
            self.assertIn(b'<strong>testuser</strong>', response.data)
