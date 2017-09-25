from sqlalchemy.exc import IntegrityError

from app import db
from app.api.models import User
from tests.base import BaseTestCase
from tests.utils import add_user


class TestUserModel(BaseTestCase):
    """Validate our User model."""

    def test_add_user(self):
        user = add_user('test', 'test@mail.com', 'test')
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'test')
        self.assertEqual(user.email, 'test@mail.com')
        self.assertTrue(user.active)
        self.assertTrue(user.password)
        self.assertTrue(user.created_at)

    def test_add_duplicate_username(self):
        add_user('test', 'test@mail.com', 'test')
        duplicate_user = User(
            username='test',
            email='test@mail2.com',
            password='test'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_duplicate_email(self):
        add_user('test', 'test@mail.com', 'test')
        duplicate_user = User(
            username='test2',
            email='test@mail.com',
            password='test'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_passwords_are_random(self):
        user_one = add_user('test', 'test@test.com', 'test')
        user_two = add_user('test2', 'test@test2.com', 'test')
        self.assertNotEqual(user_one.password, user_two.password)
