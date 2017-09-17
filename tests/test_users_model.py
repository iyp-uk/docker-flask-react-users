from sqlalchemy.exc import IntegrityError

from app import db
from app.api.models import User
from tests.base import BaseTestCase
from tests.utils import add_user


class TestUserModel(BaseTestCase):
    """Validate our User model."""

    def test_add_user(self):
        user = add_user('test', 'test@mail.com')
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'test')
        self.assertEqual(user.email, 'test@mail.com')
        self.assertTrue(user.active)
        self.assertTrue(user.created_at)

    def test_add_duplicate_username(self):
        add_user('test', 'test@mail.com')
        duplicate_user = User(
            username='test',
            email='test@mail2.com'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_duplicate_email(self):
        add_user('test', 'test@mail.com')
        duplicate_user = User(
            username='test2',
            email='test@mail.com'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)
