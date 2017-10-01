# app/__init__.py
import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# instantiate the extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)

    # enable CORS
    CORS(app)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from app.api.views.users import users_blueprint
    app.register_blueprint(users_blueprint)
    from app.api.views.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
