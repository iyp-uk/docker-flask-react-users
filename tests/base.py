from flask_testing import TestCase
from app import create_app, db

app = create_app()


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object('app.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def register(self, data):
        with self.client:
            return self.client.post(
                '/auth/register',
                data=data,
                content_type='application/json'
            )

    def post_user(self, data):
        with self.client:
            return self.client.post(
                '/users',
                data=data,
                content_type='application/json'
            )
