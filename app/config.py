# app/config.py
import os


class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SECRET_KEY = 'my_precious'
    BCRYPT_LOG_ROUNDS = 13
    JWT_EXPIRATION_TIME_SECONDS = os.environ.get('JWT_EXPIRATION_TIME_SECONDS', 3600)


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4


class TestingConfig(BaseConfig):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')
    BCRYPT_LOG_ROUNDS = 4
    JWT_EXPIRATION_TIME_SECONDS = 1


class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False
