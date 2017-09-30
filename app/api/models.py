import datetime

import jwt
from flask import current_app
from sqlalchemy import exc
from sqlalchemy.orm.exc import NoResultFound

from app import db, bcrypt


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, email, password, created_at=datetime.datetime.utcnow()):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.created_at = created_at

    def save(self):
        if not self.username or not self.email or not self.password:
            raise ValueError
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise

    @staticmethod
    def login(email, password):
        if not email or not password:
            raise ValueError
        try:
            user = User.query.filter_by(email=email).one()
        except NoResultFound:
            raise
        if not bcrypt.check_password_hash(user.password, password):
            raise NoResultFound
        return user

    def get_data(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at
        }

    @staticmethod
    def get_by_id(user_id):
        """Gets a user by its id"""
        try:
            user = User.query.get(user_id)
        except exc.DataError:
            return None
        return None if not user else user.get_data()

    @staticmethod
    def get_all_users():
        """Returns all users"""
        users_list = []
        for user in User.query.order_by(User.created_at.desc()).all():
            users_list.append(user.get_data())
        return users_list

    @staticmethod
    def encode_auth_token(user_id):
        """Encodes the JWT based on user id
        :rtype: bytes|string
        :param user_id: the user id
        :return: encoded JWT
        """
        try:
            payload = {
                # Expiration Time Claim (exp)
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=current_app.config.get('JWT_EXPIRATION_TIME_SECONDS')),
                # Issued At Claim (iat)
                'iat': datetime.datetime.utcnow(),
                # Subject (sub)
                'sub': user_id
            }
            return jwt.encode(payload, current_app.config.get('SECRET_KEY'), algorithm='HS256')
        except Exception:
            return 'Could not encode token.'

    @staticmethod
    def decode_auth_token(auth_token):
        """Decodes auth token
        """
        try:
            payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'), algorithms='HS256')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Expired token, please login again.'
        except jwt.InvalidTokenError:
            return 'Invalid token'
        except Exception:
            return 'Could not decode token.'
