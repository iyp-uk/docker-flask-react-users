import unittest
import os
from flask import current_app
from flask_testing import TestCase
from app import create_app

app = create_app()


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('app.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'my_precious')
        self.assertTrue(app.config['DEBUG'])
        self.assertFalse(app.config['TESTING'])
        self.assertFalse(current_app is None)
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get('DATABASE_URL'))
        self.assertTrue(
            app.config['JWT_EXPIRATION_TIME_SECONDS'] == os.environ.get('JWT_EXPIRATION_TIME_SECONDS ', 3600))


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('app.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'my_precious')
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(app.config['TESTING'])
        self.assertFalse(current_app is None)
        self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get('TEST_DATABASE_URL'))
        self.assertTrue(app.config['JWT_EXPIRATION_TIME_SECONDS'] == 1)


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('app.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'my_precious')
        self.assertFalse(app.config['DEBUG'])
        self.assertFalse(app.config['TESTING'])
        self.assertTrue(
            app.config['JWT_EXPIRATION_TIME_SECONDS'] == os.environ.get('JWT_EXPIRATION_TIME_SECONDS ', 3600))


if __name__ == '__main__':
    unittest.main()
