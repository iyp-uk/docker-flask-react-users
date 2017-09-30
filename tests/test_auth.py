import json

from app.api.models import User
from tests.base import BaseTestCase
from tests.constants import *


class TestAuth(BaseTestCase):
    def test_user_registration(self):
        response = self.register(json.dumps(USER_BASIC))
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['data']['username'] == 'test')
        self.assertTrue(data['token'])
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 201)

    def test_user_registration_no_username(self):
        response = self.register(json.dumps(USER_NO_USERNAME))
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'error')
        self.assertTrue(data['message'] == 'Invalid payload.')

    def test_user_registration_no_email(self):
        response = self.register(json.dumps(USER_NO_EMAIL))
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'error')
        self.assertTrue(data['message'] == 'Invalid payload.')

    def test_user_registration_no_password(self):
        response = self.register(json.dumps(USER_NO_PASSWORD))
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'error')
        self.assertTrue(data['message'] == 'Invalid payload.')

    def test_user_registration_duplicate_username(self):
        User(**USER_BASIC).save()
        response = self.register(json.dumps(USER_DUPLICATE_USERNAME))
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'error')
        self.assertTrue(data['message'] == 'User already exists.')

    def test_user_registration_duplicate_email(self):
        User(**USER_BASIC).save()
        response = self.register(json.dumps(USER_DUPLICATE_EMAIL))
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'error')
        self.assertTrue(data['message'] == 'User already exists.')
