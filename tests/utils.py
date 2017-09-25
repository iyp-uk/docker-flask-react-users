import datetime

from app.api.models import User
from app import db


def add_user(username, email, password, created_at=datetime.datetime.utcnow()):
    """Adds a single user"""
    user = User(
        username=username,
        email=email,
        password=password,
        created_at=created_at
    )
    db.session.add(user)
    db.session.commit()
    return user
